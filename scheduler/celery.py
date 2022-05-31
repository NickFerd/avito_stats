"""Celery based tasks and application"""

from celery import Celery
from celery.schedules import schedule
from redbeat import RedBeatSchedulerEntry

from config import settings
from service.tasks import etl_avito_stats

app = Celery(__name__)

app.conf.broker_url = settings.celery_broker_url
app.conf.result_backend = settings.celery_broker_url
app.conf.update({
    'redbeat_redis_url': settings.redbeat_redis_url
})


@app.task
def get_stats(pair_id: str):
    """Get stat for provided pair_id item"""
    etl_avito_stats(pair_id)


class RedBeatCeleryScheduler:
    """Wrapper around redbeat-redis scheduler
    """
    prefix = 'redbeat:'
    callable = settings.task_path

    def __init__(self, app: Celery):
        self.app = app

    def add_task(self, task_name: str, check_every_minute: int):
        """Update existing or add a new task to periodic schedule"""
        check_every_seconds = check_every_minute * 60
        interval = schedule(run_every=check_every_seconds)
        entry = RedBeatSchedulerEntry(task_name,
                                      self.callable,
                                      interval,
                                      kwargs={'pair_id': task_name},
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
