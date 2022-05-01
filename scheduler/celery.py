"""Celery based tasks and application"""
import os

from celery import Celery
from service.tasks import get_stats

import redbeat.schedulers as sh

app = Celery(__name__)

app.conf.broker_url = os.environ.get('CELERY_BROKER_URL',
                                     'redis://localhost:6379')
app.conf.result_backend = os.environ.get('CELERY_BROKER_URL',
                                         'redis://localhost:6379')
app.conf.update({
    'redbeat_redis_url': os.environ.get('REDBEAT_REDIS_URL',
                                        "redis://localhost:6379/1")
})


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(30, simple_task.s(), name='simple task')

@app.task
def simple_task():
    """test task"""
    get_stats()
    return True
