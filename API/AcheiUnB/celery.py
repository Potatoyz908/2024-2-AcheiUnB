from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcheiUnB.AcheiUnB.settings')

app = Celery('AcheiUnb')

# Carrega configurações do Celery do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tasks automaticamente
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
