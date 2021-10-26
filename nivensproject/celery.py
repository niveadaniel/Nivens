import os

from celery import Celery
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Path do módulo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nivensproject.settings')

# Criação do objeto
app = Celery('nivensproject')

# Configuração do objeto
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'])

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# run celery local:
# celery -A nivensproject worker -l INFO
