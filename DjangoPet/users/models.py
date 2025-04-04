from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Propietario(models.Model):
    """
    Los campos como nombre, apellido y correo estan en el modelo User como:
     first_name, last_name y email.
    """

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="propietario"
    )
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=15, null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    @property
    def nombre(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"


class Veterinario(models.Model):
    """
    Los campos como nombre, apellido y correo estan en el modelo User como:
     first_name, last_name y email.
    """

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="veterinario"
    )
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    especializacion = models.CharField(max_length=100)
    disponibilidad = models.TextField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.especializacion}"

    @property
    def nombre(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    def get_absolute_url(self):
        return reverse("users:veterinario_detail", args=[str(self.id)])
