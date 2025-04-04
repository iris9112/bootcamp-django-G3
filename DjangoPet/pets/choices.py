from django.db import models


class GeneroChoices(models.TextChoices):
    MACHO = "Macho"
    HEMBRA = "Hembra"


class EstadoMascotaChoices(models.TextChoices):
    ACTIVO = "ACTIVO"
    FALLECIDO = "FALLECIDO"
    EN_TRATAMIENTO = "EN_TRATAMIENTO"
