"""
File containing functions to be executed by background workers
(like celery, etc)
"""

import requests
from hyper.contrib import HTTP20Adapter

from database.base import LocalSession
from database import crud
import utils
from config import settings


def etl_avito_stats(pair_id: str):
    """Get current number of ads and top 5 for this pair of query and
    location
    """
    with LocalSession() as session:
        with session.begin():
            pair_object = crud.get_pair_by_id(session, pair_id=pair_id)
            query = pair_object.query
            location = pair_object.location
            location_id = utils.get_valid_locations().get(location)
            if not location_id:
                raise KeyError(f'Invalid location - {location}')

            raw_data = fetch_from_avito_api(location_id=location_id,
                                            query=query)
            # todo


def fetch_from_avito_api(location_id: int, query: str) -> dict:
    """Fetch data from api"""
    base_url = settings.avito_api_base_url
    params = {
        "locationId": location_id,
        "name": query
    }
    session = requests.Session()
    session.mount('https://', HTTP20Adapter())
    result = session.get(base_url, params=params)
    result.raise_for_status()
    result = result.json()

    print('count', result['count'], sep=' ')
    print('totalCount', result['totalCount'], sep=' ')
    print('totalElements', result['totalElements'], sep=' ')
    print('mainCount', result['mainCount'], sep=' ')
    print('len items', len(result['catalog']['items']), sep=' ')

    return result


if __name__ == '__main__':
    fetch_from_avito_api(location_id=622470, query='Трэкбол')
