"""
File containing functions to be executed by background workers
(like celery, etc)
"""
from datetime import datetime
from typing import List

import requests
from hyper.contrib import HTTP20Adapter

import utils
from config import settings
from database import crud
from database.base import LocalSession
from service.utils import StatItem, AdItem


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

            stat_item = process_data(raw_data=raw_data, pair_id=pair_id)
            crud.create_stat(session, stat_item=stat_item)


def fetch_from_avito_api(location_id: int, query: str) -> dict:
    """Fetch data from api"""
    base_url = settings.avito_api_base_url
    params = {
        "locationId": location_id,
        "name": query
    }
    session = requests.Session()
    # noinspection PyTypeChecker
    session.mount('https://', HTTP20Adapter())
    result = session.get(base_url, params=params)
    result.raise_for_status()
    result = result.json()

    return result


def process_data(raw_data: dict, pair_id: str) -> StatItem:
    """Get needed info from raw data to fill StatItem"""
    moment = datetime.utcnow()
    count = raw_data['count']
    ads = get_ads(items=raw_data['catalog']['items'])
    return StatItem(pair_id=pair_id, moment=moment, count=count, ads=ads)


def get_ads(items: dict) -> List[AdItem]:
    """Get top X ad items"""
    ads = []
    ads_count = 0
    for item in items:
        # avoid banners, not real ads
        if 'id' not in item:
            continue

        # take only limited number
        if ads_count == settings.top_ads:
            break

        ads_count += 1
        ad_id = item['id']
        title = item['title']
        price = item['priceDetailed']['value']
        url = settings.avito_base_url + item['urlPath']

        ad_item = AdItem(ad_id=ad_id, title=title, price=price,
                         url=url)
        ads.append(ad_item)

    return ads


if __name__ == '__main__':
    fetch_from_avito_api(location_id=622470, query='Трэкбол')
