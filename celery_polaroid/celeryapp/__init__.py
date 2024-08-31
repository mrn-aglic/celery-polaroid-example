import os

from celery import Celery
from celery.utils.log import get_task_logger

from . import celeryconfig
from .celeryconfig import task_queues

logger = get_task_logger(__name__)

app = Celery("celery_polaroid")

app.config_from_object(celeryconfig)

instance = os.environ.get("instance")

with open(f"{instance}.txt", "w") as f:
    f.write(f"{instance} is running")

if instance == "scheduler":
    app.control.purge()
