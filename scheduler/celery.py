"""Celery based tasks and application"""

import os

from celery import Celery
from celery.schedules import schedule
from redbeat import RedBeatSchedulerEntry

from service.tasks import get_stats


app = Celery(__name__)

app.conf.broker_url = os.environ.get('CELERY_BROKER_URL',
                                     'redis://localhost:6379')
app.conf.result_backend = os.environ.get('CELERY_BROKER_URL',
                                         'redis://localhost:6379')
app.conf.update({
    'redbeat_redis_url': os.environ.get('REDBEAT_REDIS_URL',
                                        "redis://localhost:6379/1")
})


@app.task
def simple_task():
    """test task"""
    get_stats()
    return True


class RedBeatCeleryScheduler:
    """Wrapper around redbeat-redis scheduler
    """
    prefix = 'redbeat:'

    def __init__(self, app: Celery):
        self.app = app

    def add_task(self, task_name: str, check_every_minute: int):
        """Update existing or add a new task to periodic schedule"""
        check_every_seconds = check_every_minute * 60
        interval = schedule(run_every=check_every_seconds)
        entry = RedBeatSchedulerEntry(task_name,
                                      'scheduler.celery.simple_task',  # fixme
                                      interval,
                                      app=self.app)
        entry.save()
        return entry

    def stop_task(self, task_name: str):
        """Delete task from periodic schedule
        """
        task_name = f'{self.prefix}{task_name}'
        try:
            entry = RedBeatSchedulerEntry.from_key(key=task_name, app=self.app)
        except KeyError:
            raise
        entry.enabled = False
        entry.save()
        return entry


