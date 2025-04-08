from celery import shared_task

@shared_task
def enviar_recordatorio():
    print("Recordatorio enviado!")
    return "Recordatorio enviado!"
