"""Dependency functions used in web application"""

from database.base import LocalSession
from scheduler import celery
from scheduler.celery import RedBeatCeleryScheduler
import utils
from service.stats_service import StatsService


def init_service():
    """Instantiate service and all needed components
    """
    scheduler = RedBeatCeleryScheduler(app=celery.app)
    service = StatsService(scheduler=scheduler,
                           db_session=LocalSession)
    return service


def valid_locations():
    """Preheat cache
    """
    return utils.get_valid_locations()
