import os

from celery import Celery
# Path do módulo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nivensproject.settings')

# Criação do objeto
app = Celery('nivensproject')

# Configuração do objeto
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# run celery local:
# celery -A nivensproject worker -l INFO
