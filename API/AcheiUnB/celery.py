from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configurações padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcheiUnB.settings')

# Instancia o Celery
app = Celery('AcheiUnB')

# Carrega as configurações do Django no Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tasks registradas em INSTALLED_APPS
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')