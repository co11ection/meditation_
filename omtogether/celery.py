import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omtogether.settings")

app = Celery("omtogether")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
