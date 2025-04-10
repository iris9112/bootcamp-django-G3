import csv
import os
import time
import random

from django.conf import settings

from celery import shared_task
from pets.models import FichaMedica, Mascota


@shared_task(name="crear_ficha_medica")
def crear_ficha_medica(mascota_id):
    print("INFO - Creando ficha medica")
    mascota = Mascota.objects.get(id=mascota_id)
    if not hasattr(mascota, "ficha_medica"):
        FichaMedica.objects.create(
            mascota=mascota,
            descripcion="Ficha creada automáticamente por cambio de estado.",
        )


@shared_task
def generar_historial_mascota_csv(mascota_id):
    try:
        mascota = Mascota.objects.select_related("ficha_medica", "propietario").get(id=mascota_id)
    except Mascota.DoesNotExist:
        return f"Mascota con ID {mascota_id} no encontrada."

    # Simulación de demora en el procesamiento
    delay = random.randint(1, 6)
    time.sleep(delay)

    export_dir = os.path.join(settings.MEDIA_ROOT, "reportes")
    file_path = os.path.join(export_dir, f"historial_{mascota.id}.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Campo", "Valor"])
        writer.writerow(["Nombre", mascota.nombre])
        writer.writerow(["Especie", mascota.especie])
        writer.writerow(["Raza", mascota.raza])
        writer.writerow(["Género", mascota.genero])
        writer.writerow(["Color", mascota.color])
        writer.writerow(["Peso", mascota.peso])
        writer.writerow(["Fecha de nacimiento", mascota.fecha_nacimiento or "N/A"])
        writer.writerow(["Esterilizado", "Sí" if mascota.esterilizado else "No"])
        writer.writerow(["N° Microchip", mascota.numero_microchip])
        writer.writerow(["Fecha último control", mascota.fecha_ultimo_control or "N/A"])
        writer.writerow(["Estado", mascota.estado])
        writer.writerow(["Propietario", mascota.propietario.nombre])
        writer.writerow(["Fecha creación", mascota.created_at])
        writer.writerow(["Fecha modificación", mascota.updated_at])

        if hasattr(mascota, "ficha_medica"):
            writer.writerow([])
            writer.writerow(["-- Información médica --"])
            writer.writerow(["Número de ficha", mascota.ficha_medica.numero_ficha])
            writer.writerow(["Descripción", mascota.ficha_medica.descripcion])
            writer.writerow(["Alergias", mascota.ficha_medica.alergias or "N/A"])
            writer.writerow(["Vacunas", mascota.ficha_medica.vacunas or "N/A"])
            writer.writerow(["Desparasitado", "Sí" if mascota.ficha_medica.desparasitado else "No"])
            writer.writerow(["Fecha desparasitación", mascota.ficha_medica.fecha_desparasitacion or "N/A"])
            writer.writerow(["Observaciones", mascota.ficha_medica.observaciones or "N/A"])
            writer.writerow(["Creada", mascota.ficha_medica.created_at])
            writer.writerow(["Última actualización", mascota.ficha_medica.updated_at])

    return f"Reporte generado exitosamente para {mascota.nombre} (ID: {mascota.id})"

