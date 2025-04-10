from django.db.models.signals import post_save
from django.dispatch import receiver

from pets.choices import EstadoMascotaChoices
from pets.models import Mascota
from pets.tasks import crear_ficha_medica


@receiver(post_save, sender=Mascota)
def crear_ficha_si_esta_en_tratamiento(sender, instance, created, **kwargs):
    try:
        old = Mascota.objects.get(pk=instance.pk)
    except Mascota.DoesNotExist:
        return

    if (
        old.estado != instance.estado
        and instance.estado == EstadoMascotaChoices.EN_TRATAMIENTO
    ):
        crear_ficha_medica.delay(instance.id)
