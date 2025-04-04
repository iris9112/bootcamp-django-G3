from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from pets.choices import EstadoMascotaChoices
from pets.models import Mascota
from users.models import User, Propietario


class TestMascotaListView(TestCase):

    def setUp(self):
        for i in range(10):
            propietario = G(Propietario, usuario=G(User))
            G(
                Mascota,
                propietario=propietario,
                estado=(
                    EstadoMascotaChoices.FALLECIDO
                    if i == 7
                    else EstadoMascotaChoices.ACTIVO
                ),
            )

        self.url = reverse("pets:mascota_list")

    def test_mascota_list(self):
        response = self.client.get(self.url)
        mascotas = response.context["mascotas"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mascotas), 6)
        self.assertTrue(response.context["is_paginated"])
        self.assertTemplateUsed(response, "pets/mascota_list.html")
