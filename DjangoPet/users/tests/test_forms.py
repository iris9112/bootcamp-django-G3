from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Veterinario
from users.forms import VeterinarioForm


class VeterinarioFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "dra_huellitas",
            "first_name": "Ana",
            "last_name": "Ramírez",
            "email": "dr.huellitas@example.com",
            "identificacion": "123456789",
            "telefono": "3200000000",
            "especializacion": "Felinos",
            "disponibilidad": "Lunes a Viernes",
        }

        self.invalid_data = {
            "username": "dra_huellitas",
            "first_name": "Ana",
            "last_name": "Ramírez",
            "telefono": "3200000000",
            "especializacion": "Felinos",
            "disponibilidad": "Lunes a Viernes",
            "matricula": "123456789",
        }

    def test_form_is_valid(self):
        self.assertEqual(Veterinario.objects.count(), 0)
        self.assertEqual(User.objects.all().count(), 0)

        form = VeterinarioForm(self.valid_data)
        self.assertTrue(form.is_valid())

        veterinario = form.save()
        self.assertEqual(Veterinario.objects.count(), 1)
        self.assertEqual(User.objects.all().count(), 1)

        self.assertTrue(veterinario.activo)

        user = User.objects.get(username="dra_huellitas")
        self.assertEqual(user.username, "dra_huellitas")
        self.assertEqual(veterinario.usuario, user)

    def test_form_is_invalid(self):
        form = VeterinarioForm(self.invalid_data)
        self.assertFalse(form.is_valid())
