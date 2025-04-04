from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import first
from django.test import TestCase
from django.utils import timezone
from django_dynamic_fixture import G
from freezegun import freeze_time

from appointments.choices import EstadoCitaChoices
from appointments.models import Consulta
from pets.models import Mascota
from users.models import Veterinario


class TestConsulta(TestCase):

    @freeze_time("2023-12-01 10:00:00")
    def setUp(self):
        self.veterinario = G(
            Veterinario, usuario=G(User, first_name="Ana", last_name="Perez")
        )
        self.mascota = G(
            Mascota,
            nombre="Firulais",
        )

        self.consulta = G(
            Consulta,
            veterinario=self.veterinario,
            mascota=self.mascota,
            fecha_consulta=timezone.now(),
            motivo="Chequeo general",
            requiere_control=False,
        )

    def test_creacion_consulta(self):
        self.assertEqual(Consulta.objects.count(), 1)
        self.assertEqual(self.consulta.mascota, self.mascota)
        self.assertEqual(self.consulta.veterinario, self.veterinario)
        self.assertEqual(self.consulta.estado_cita, EstadoCitaChoices.ACTIVA)
        self.assertEqual(self.consulta.duracion, 30)

        expected_str = "Consulta 1 - Firulais con Dr. Ana Perez (01/12/2023 10:00)"
        self.assertEqual(self.consulta.__str__(), expected_str)

    @freeze_time("2023-12-01 10:00:00")
    def test_validacion_consulta(self):
        consulta_duplicada = Consulta(
            veterinario=self.veterinario,
            mascota=self.mascota,
            fecha_consulta=timezone.now(),
            motivo="Chequeo general",
            requiere_control=False,
        )

        with self.assertRaises(ValidationError) as e:
            consulta_duplicada.clean()

        self.assertIn(
            "Ya existe una consulta para este veterinario en la misma fecha y hora.",
            str(e.exception),
        )

    @freeze_time("2023-12-01 10:00:00")
    def test_consulta_signal(self):
        self.assertEqual(Consulta.objects.count(), 1)

        self.consulta.requiere_control = True
        self.consulta.save()

        self.assertEqual(Consulta.objects.count(), 2)
        self.assertTrue(
            Consulta.objects.filter(motivo="Consulta de control automática").exists()
        )
