from django.db import models


class EstadoCitaChoices(models.TextChoices):
    ACTIVA = "ACTIVA", "Activa"
    CANCELADA = "CANCELADA", "Cancelada"
    REPROGRAMADA = "REPROGRAMADA", "Reprogramada"
    COMPLETADA = "COMPLETADA", "Completada"


class UnidadTemperaturaChoices(models.TextChoices):
    CELSIUS = "C", "Celsius"
    FAHRENHEIT = "F", "Fahrenheit"


class UnidadPesoChoices(models.TextChoices):
    KILOGRAMOS = "KG", "Kilogramos"
    LIBRAS = "LB", "Libras"
