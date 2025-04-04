from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from .models import Consulta


@receiver(pre_save, sender=Consulta)
def crear_consulta_control(sender, instance, **kwargs):
    """Verifica si una consulta requiere control, y de ser así
    crea una nueva consulta automáticamente para dentro de 25 dias
    a la misma hora, con el mismo profesional"""

    print("****** Creando consulta control")

    if instance.pk:
        # Recuperar el estado anterior desde la BD
        old_instance = Consulta.objects.get(pk=instance.pk)

        # Si antes era False y ahora es True
        if not old_instance.requiere_control and instance.requiere_control:
            nueva_fecha = instance.fecha_consulta + timedelta(days=25)

            # Evitar duplicados si ya existe una consulta de control igual
            existe_control = Consulta.objects.filter(
                veterinario=instance.veterinario,
                mascota=instance.mascota,
                fecha_consulta=nueva_fecha,
            ).exists()

            if not existe_control:
                Consulta.objects.create(
                    mascota=instance.mascota,
                    veterinario=instance.veterinario,
                    fecha_consulta=nueva_fecha,
                    duracion=instance.duracion,
                    motivo="Consulta de control automática",
                    descripcion="Generada automáticamente 25 días después.",
                    costo_consulta=instance.costo_consulta,
                    requiere_control=False,
                )
