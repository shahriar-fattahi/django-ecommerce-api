from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault("DJANGO_SETTING_MODULE", "src.settings")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")


celery_app = Celery("src")
celery_app.autodiscover_tasks()
celery_app.conf.broker_url = CELERY_BROKER_URL
celery_app.conf.result_backend = "rcp://"
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = [
    "json",
]
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4
