"""Helping functions
"""

import requests


def process_locations(endpoint: str):
    """Get and transform locations IDs from external API"""
    result = dict()
    base_url = "https://rest-app.net/api/"
    url = base_url + endpoint
    res = requests.get(url)
    res.raise_for_status()
    raw_result = res.json()['data']
    for location in raw_result:
        result[location["name"]] = location["id"]

    return result
