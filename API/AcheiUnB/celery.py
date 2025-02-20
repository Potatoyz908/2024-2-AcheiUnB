from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define a configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API.AcheiUnB.settings")

app = Celery("AcheiUnB")


# Carrega as configurações do Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobre tasks automaticamente nos apps instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
