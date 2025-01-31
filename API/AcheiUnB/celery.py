from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Define o módulo de configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API.AcheiUnB.settings")

app = Celery("AcheiUnB")

# Carrega as configurações do Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobrir tasks automaticamente em aplicativos registrados
app.autodiscover_tasks()
