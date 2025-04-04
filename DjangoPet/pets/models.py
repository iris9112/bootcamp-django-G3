from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from users.models import Propietario
from pets.choices import GeneroChoices, EstadoMascotaChoices


class Mascota(models.Model):
    propietario = models.ForeignKey(
        Propietario, on_delete=models.CASCADE, related_name="mascotas"
    )
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GeneroChoices.choices)
    color = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to="mascotas/", null=True, blank=True)
    esterilizado = models.BooleanField(default=False)
    numero_microchip = models.CharField(max_length=30, null=True, blank=True)
    fecha_ultimo_control = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=30,
        choices=EstadoMascotaChoices.choices,
        default=EstadoMascotaChoices.ACTIVO,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.especie} ({self.propietario})"

    def get_absolute_url(self):
        return reverse("pets:mascota_detail", args=[str(self.id)])

    @property
    def propietario_nombre(self):
        return str(self.propietario.nombre)

    @property
    def edad_categoria(self):
        if not self.fecha_nacimiento:
            return "Desconocida"

        hoy = now().date()
        edad = (
            hoy.year
            - self.fecha_nacimiento.year
            - (
                (hoy.month, hoy.day)
                < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        )

        if edad < 1:
            return "Cachorro"
        elif 1 <= edad < 7:
            return "Adulto"
        else:
            return "Senior"


class FichaMedica(models.Model):
    numero_ficha = models.PositiveIntegerField(unique=True, editable=False)
    mascota = models.OneToOneField(
        Mascota, on_delete=models.CASCADE, related_name="ficha_medica"
    )
    descripcion = models.TextField()
    alergias = models.CharField(max_length=255, null=True, blank=True)
    vacunas = models.CharField(max_length=255, null=True, blank=True)
    desparasitado = models.BooleanField(default=False)
    fecha_desparasitacion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.numero_ficha:
            ultima_ficha = FichaMedica.objects.order_by("-numero_ficha").first()
            self.numero_ficha = ultima_ficha.numero_ficha + 1 if ultima_ficha else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ficha médica de {self.mascota.nombre}"
