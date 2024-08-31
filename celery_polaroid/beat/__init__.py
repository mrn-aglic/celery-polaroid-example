from celery.utils.log import get_task_logger

from celery_polaroid.app import config
from celery_polaroid.celeryapp import app
from celery_polaroid.worker.test_tasks import delayed_tasks_pipeline, simple_pipeline
from celery_polaroid.worker.test_tasks.delayed_tasks_pipeline import producer

logger = get_task_logger(__name__)

if config.is_dev():
    import logging

    logging.basicConfig(level=logging.INFO)


def schedule_simple_pipeline(num, countdown=5):
    for _ in range(num):
        simple_pipeline.pipeline.s().apply_async(countdown=countdown)


def schedule_delayed_pipeline(num, countdown=5):
    for i in range(num):
        delayed_tasks_pipeline.pipeline.s().apply_async(countdown=countdown * (i + 1))


def schedule_multiple_sleeping_single_tasks(num, countdown=5):
    for _ in range(num):
        # producer.s().apply_async(countdown=countdown * (i + 1))
        producer.s().apply_async(countdown=countdown)


def periodic_delayed_tasks_pipeline(sender, schedule: int = 3):
    sender.add_periodic_task(
        sig=delayed_tasks_pipeline.pipeline.s(),
        name="delayed_tasks_pipeline",
        schedule=schedule,
    )


def periodic_delayed_tasks_pipeline_producer(sender, schedule: int = 3):
    sender.add_periodic_task(
        sig=delayed_tasks_pipeline.producer.s(),
        name="delayed_tasks_pipeline_producer",
        schedule=schedule,
    )


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        logger.info("SETUP TASKS")

        run_examples = {
            "schedule_simple_pipeline": False,
            "schedule_delayed_pipeline": True,
            "schedule_multiple_sleeping_single_tasks": False,
            "periodic_delayed_tasks_pipeline": False,
            "periodic_delayed_tasks_pipeline_producer": False,
        }

        if run_examples["schedule_simple_pipeline"]:
            schedule_simple_pipeline(num=5)

        if run_examples["schedule_delayed_pipeline"]:
            schedule_delayed_pipeline(num=2)

        if run_examples["schedule_multiple_sleeping_single_tasks"]:
            schedule_multiple_sleeping_single_tasks(num=15)

        if run_examples["periodic_delayed_tasks_pipeline"]:
            periodic_delayed_tasks_pipeline(sender)

        if run_examples["periodic_delayed_tasks_pipeline_producer"]:
            periodic_delayed_tasks_pipeline_producer(sender)

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
