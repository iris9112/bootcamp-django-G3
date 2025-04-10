import time
import random
from celery import shared_task

@shared_task
def enviar_recordatorio():
    seconds = random.randint(1, 10)
    time.sleep(seconds)
    print(f"INFO - Recordatorio enviado! ****Tomo {seconds} segundo(s)****")
    return f"Recordatorio # enviado"
