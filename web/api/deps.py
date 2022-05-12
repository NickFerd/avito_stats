"""Dependency functions used in web application"""

from scheduler import celery
from scheduler.celery import RedBeatCeleryScheduler
from service.stats_service import StatsService
from database.base import LocalSession


def init_service():
    """Instantiate service and all needed components
    """
    scheduler = RedBeatCeleryScheduler(app=celery.app)
    service = StatsService(scheduler=scheduler,
                           db_session=LocalSession)
    return service
