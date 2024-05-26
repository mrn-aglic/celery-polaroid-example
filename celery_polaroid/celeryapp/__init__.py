import os

from celery import Celery

from . import celeryconfig
from .celeryconfig import task_queues

app = Celery("celery_polaroid")

app.config_from_object(celeryconfig)

instance = os.environ.get("instance")

if instance == "scheduler":
    app.control.purge()
