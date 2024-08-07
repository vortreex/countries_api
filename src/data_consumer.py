"""
This module contains function for retreiwing data from remote API host.
"""
from functools import lru_cache
import requests

_REQUEST_TIMEOUT = 10
_CACHE_CAPACITY = 5
_COUNTRIES_API_HOST = 'https://restcountries.com/v3.1'
_COUNTRY_PARAMS = {'fields': ['name' ,'capital', 'region', 'subregion',
                              'population', 'area', 'borders']}


def _send_request(host: str = _COUNTRIES_API_HOST) -> dict | list:
    """
    Function that handles sending the request to remote API Host.
    :param: Remote API Host URL
    :return: JSON like object (dictionary or list) containing retrieved data.
    """

    response = requests.get(url=host, timeout=_REQUEST_TIMEOUT, params=_COUNTRY_PARAMS)
    response.raise_for_status()
    data = response.json()
    return data

def _sanitize_data(data: list) -> list:
    """
    Function that sanitizes retrieved data by removing redundant country names
    and flattens single element lists. The index error may occure as some countries
    might not have specified capital.
    :param: Unsanitized data
    :return: Sanitized data
    """
    for country in data:
        country['name'] = country['name']['common']
        try:
            country['capital'] = country['capital'][0]
        except IndexError:
            country['capital'] = country['name']

    return data

@lru_cache(maxsize=_CACHE_CAPACITY)
def send_region_request(region: str) -> list:
    """
    Function that sends REST API request to remote host in order
    to retrieve data about countries in specified region and caches it.
    :param region: Region name
    :return : List of dictionaries containing information about countries in region
    """
    data = _send_request(host=f'{_COUNTRIES_API_HOST}/region/{region}')
    return _sanitize_data(data)

@lru_cache(maxsize=_CACHE_CAPACITY)
def send_subregion_request(subregion: str) -> list:
    """
    Function that sends REST API request to remote host in order
    to retrieve data about countries in specified subregion and caches it.
    :param region: Region name
    :return : List of dictionaries containing information about countries in subregion
    """
    data = _send_request(host=f'{_COUNTRIES_API_HOST}/subregion/{subregion}')
    return _sanitize_data(data)
