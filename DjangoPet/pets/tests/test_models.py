import unittest
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django_dynamic_fixture import G

from pets.choices import GeneroChoices
from pets.models import Mascota
from users.models import Propietario


@unittest.skip
class MascotaTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create(
            first_name="Jon",
            last_name="Bonachon",
            email="jon@test.com",
        )
        self.propietario = Propietario.objects.create(
            usuario=self.usuario, identificacion="111456", telefono="+57 300-224-7878"
        )

        self.garfield = Mascota.objects.create(
            propietario=self.propietario,
            nombre="Garfield",
            especie="Gato",
            raza="Americano común",
            genero=GeneroChoices.MACHO,
            color="naranja",
            peso=7.5,
            esterilizado=True,
        )

    def test_crear_mascota(self):
        self.assertEqual(Mascota.objects.count(), 1)

        self.assertEqual(self.garfield.propietario.nombre, "Jon Bonachon")
        expected_str = f"Garfield - Gato (Jon Bonachon)"
        self.assertEqual(expected_str, str(self.garfield))

        self.assertEqual(self.garfield.propietario_nombre, "Jon Bonachon")
        self.assertEqual(self.garfield.edad_categoria, "Desconocida")

    def test_edad_cachorro(self):
        self.garfield.fecha_nacimiento = timezone.now() - timedelta(days=100)
        self.garfield.save()
        self.assertEqual(self.garfield.edad_categoria, "Cachorro")

    def test_edad_senior(self):
        self.garfield.fecha_nacimiento = timezone.now() - timedelta(weeks=500)
        self.garfield.save()
        self.assertEqual(self.garfield.edad_categoria, "Senior")


class MascotaFixtureTest(TestCase):

    def setUp(self):
        self.usuario = G(User, first_name="Jon", last_name="Bonachon")
        self.propietario = G(Propietario, usuario=self.usuario)
        self.garfield = G(
            Mascota,
            propietario=self.propietario,
            nombre="Garfield",
            especie="Gato",
        )

    def test_crear_mascota(self):
        self.assertEqual(Mascota.objects.count(), 1)

        self.assertEqual(self.garfield.propietario.nombre, "Jon Bonachon")
        expected_str = f"Garfield - Gato (Jon Bonachon)"
        self.assertEqual(expected_str, str(self.garfield))

        self.assertEqual(self.garfield.propietario_nombre, "Jon Bonachon")
        self.assertEqual(self.garfield.edad_categoria, "Desconocida")

    def test_edad_cachorro(self):
        self.garfield.fecha_nacimiento = timezone.now() - timedelta(days=100)
        self.garfield.save()
        self.assertEqual(self.garfield.edad_categoria, "Cachorro")

    def test_edad_senior(self):
        self.garfield.fecha_nacimiento = timezone.now() - timedelta(weeks=500)
        self.garfield.save()
        self.assertEqual(self.garfield.edad_categoria, "Senior")
