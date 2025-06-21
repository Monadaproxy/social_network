from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

app = Celery('social_network')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'amqp://guest:guest@localhost:5672//'
app.conf.result_backend = 'rpc://'