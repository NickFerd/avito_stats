"""Dependency functions used in web application"""

import requests
from requests.exceptions import HTTPError
from cachetools import cached, TTLCache

from database.base import LocalSession
from scheduler import celery
from scheduler.celery import RedBeatCeleryScheduler
from service.stats_service import StatsService
from web import constants
from web import utils


def init_service():
    """Instantiate service and all needed components
    """
    scheduler = RedBeatCeleryScheduler(app=celery.app)
    service = StatsService(scheduler=scheduler,
                           db_session=LocalSession)
    return service


@cached(cache=TTLCache(maxsize=constants.CACHE_SIZE, ttl=constants.CACHE_TTL))
def valid_locations():
    """Get valid locations names and their avito IDs
    Returns dict in form:
    {
    "location_name": location_id,
    ....
    }
    """

    result = dict()
    endpoints = ['region', 'city']
    for _ in range(constants.MAX_TRY):
        try:
            for endpoint in endpoints:
                result.update(utils.process_locations(endpoint))
            break
        except HTTPError:
            # Simply try again
            pass
    return result



