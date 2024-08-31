import itertools
import logging

from celery.app.control import Inspect
from celery.events.snapshot import Polaroid
from celery.events.state import State
from redis import StrictRedis

logger = logging.getLogger(__name__)


class CeleryMonitor(Polaroid):
    clear_after = True

    def emit_queue_metrics_broker_connection(self):
        logger.info("Emitting queue metrics broker connection")
        with self.app.broker_connection() as connection, connection.channel() as channel:
            queue_len = channel._size("default")
            logger.info("queue_len %d", queue_len)

    def emit_queue_metrics_strict_redis(self):
        logger.info("Emitting queue metrics with StrictRedis")
        r = StrictRedis.from_url(self.app.conf.broker_url)
        queue_name = "default"

        queue_len = r.llen(queue_name)

        logger.info("queue_len: %d", queue_len)

    def _get_active_tasks(self, inspect_instance: Inspect):
        active_tasks = inspect_instance.active()

        return [
            {
                "task_name": task["name"],
                "acknowledged": task["acknowledged"],
                "time_start": task["time_start"],
                "eta": None,
                "type": task["type"],
            }
            for task in itertools.chain(*active_tasks.values())
        ]

    def _get_reserved_tasks(self, inspect_instance: Inspect):
        reserved_tasks = inspect_instance.reserved()

        return [
            {
                "task_name": task["name"],
                "acknowledged": task["acknowledged"],
                "time_start": task["time_start"],
                "eta": None,
                "type": task["type"],
            }
            for task in itertools.chain(*reserved_tasks.values())
        ]

    def _get_scheduled_tasks(self, inspect_instance: Inspect):
        scheduled_tasks = inspect_instance.scheduled()

        return [
            {
                "task_name": task["request"]["name"],
                "acknowledged": False,
                "time_start": None,
                "eta": task["eta"],
                "type": task["request"]["type"],
            }
            for task in itertools.chain(*scheduled_tasks.values())
        ]

    def _print_task_state_by_worker(self, state):
        logger.info("Printing task state by worker:>")

        for worker, tasks in state.tasks_by_worker.items():
            logger.info("worker: %s", worker)

            for task in tasks:
                task_details = {
                    "task_name": task.name,
                    "runtime": task.runtime,
                    "timestamp": task.timestamp,
                    "state": task.state,
                    "succeeded": task.succeeded,
                    "children": [child.name for child in task.children],
                }

                logger.info("task: %s", task_details)

    def on_shutter(self, state: State):

        log_task_state_by_worker = False
        emit_queue_len_with_broker_connection = False
        emit_queue_len_with_strict_redis = True
        use_inspect_module = True

        if log_task_state_by_worker:
            logger.info("event count: %d", state.event_count)
            logger.info("task count: %d", state.task_count)

            self._print_task_state_by_worker(state)

        if emit_queue_len_with_broker_connection:
            self.emit_queue_metrics_broker_connection()

        if emit_queue_len_with_strict_redis:
            self.emit_queue_metrics_strict_redis()

        if use_inspect_module:
            inspect_instance = self.app.control.inspect()

            scheduled_tasks = self._get_scheduled_tasks(inspect_instance)
            active_tasks = self._get_active_tasks(inspect_instance)
            reserved_tasks = self._get_reserved_tasks(inspect_instance)

            logger.info("scheduled_tasks: %s", scheduled_tasks)
            logger.info("num scheduled_tasks: %d", len(scheduled_tasks))

            logger.info("active_tasks: %s", active_tasks)
            logger.info("num active_tasks: %d", len(active_tasks))

            logger.info("reserved_tasks: %s", reserved_tasks)
            logger.info("num reserved_tasks: %d", len(reserved_tasks))
