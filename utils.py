"""Helping functions
"""
from typing import Union, Sequence

import requests
from cachetools import cached, TTLCache

from config import settings

__all__ = [
    'get_valid_locations',
]


@cached(cache=TTLCache(maxsize=settings.cache_size, ttl=settings.cache_ttl))
def get_valid_locations() -> dict:
    """Get valid locations names and their avito IDs
    Returns dict in form:
    {
    "location_name": location_id,
    ....
    }
    """

    result = dict()
    endpoints = ['region', 'city']  # fixme city ids might incorrect due to repetition of cities names
    for _ in range(settings.max_retry):
        try:
            for endpoint in endpoints:
                result.update(process_locations(endpoint))
            break
        except requests.HTTPError:
            # Simply try again
            pass

    # Manually add location of russia
    russia_aliases = ['Рф', 'Россия', 'Российская федерация']
    russia_avito_id = '621540'
    result.update({alias: russia_avito_id for alias in russia_aliases})
    return result


def process_locations(endpoint: str):
    """Get and transform locations IDs from external API"""
    result = dict()
    base_url = "https://rest-app.net/api/"
    url = base_url + endpoint
    res = requests.get(url)
    res.raise_for_status()
    raw_result = res.json()['data']
    for location in raw_result:
        result[location["name"].lower()] = location["id"]

    return result


def retry_on_failure(exceptions: Union[Exception, Sequence[Exception]],
                     max_try: int):
    """Retry function if exception in :exceptions happens
    """
    pass


if __name__ == '__main__':
    """Testing"""
    process_locations('region')
    process_locations('endpoint')
