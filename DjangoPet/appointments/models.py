from django.core.exceptions import ValidationError
from django.db import models

from pets.models import Mascota
from users.models import Veterinario

from appointments.choices import (
    EstadoCitaChoices,
    UnidadTemperaturaChoices,
    UnidadPesoChoices,
)


class Consulta(models.Model):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="consultas"
    )
    veterinario = models.ForeignKey(
        Veterinario, on_delete=models.CASCADE, related_name="consultas"
    )
    fecha_consulta = models.DateTimeField()
    duracion = models.IntegerField(default=30, help_text="Duración en minutos")
    estado_cita = models.CharField(
        max_length=15,
        choices=EstadoCitaChoices.choices,
        default=EstadoCitaChoices.ACTIVA,
    )
    motivo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    unidad_temperatura = models.CharField(
        max_length=1,
        choices=UnidadTemperaturaChoices.choices,
        default=UnidadTemperaturaChoices.CELSIUS,
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    unidad_peso = models.CharField(
        max_length=2,
        choices=UnidadPesoChoices.choices,
        default=UnidadPesoChoices.KILOGRAMOS,
    )
    notas_internas = models.TextField(blank=True)
    costo_consulta = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    requiere_control = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Consulta {self.id} - {self.mascota.nombre} con Dr. {self.veterinario.nombre} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"

    def clean(self):
        super().clean()
        if (
            Consulta.objects.exclude(pk=self.pk)
            .filter(veterinario=self.veterinario, fecha_consulta=self.fecha_consulta)
            .exists()
        ):
            raise ValidationError(
                "Ya existe una consulta para este veterinario en la misma fecha y hora."
            )
