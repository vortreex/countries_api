from functools import lru_cache
import logging
import requests

_REQUEST_TIMEOUT = 10
_REQUEST_REFRESH_LIMIT = 5
_COUNTRIES_API_HOST = 'https://restcountries.com/v3.1'
_COUNTRY_PARAMS = {'fields': ['name' ,'capital', 'region', 'subregion', 'population', 'area', 'borders']}


def _send_request(host: str = _COUNTRIES_API_HOST) -> dict | list:
    """
    Function that handles sending the request to remote API Host.
    :param: Remote API Host URL
    :return: JSON like object (dictionary or list) containing retrieved data.
    """
    try:
        response = requests.get(url=host, timeout=_REQUEST_TIMEOUT, params=_COUNTRY_PARAMS)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.HTTPError as err:
        print('Error')
        raise err  

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

@lru_cache(maxsize=_REQUEST_REFRESH_LIMIT)
def send_region_request(region: str):
    data = _send_request(host=f'{_COUNTRIES_API_HOST}/region/{region}')
    return _sanitize_data(data)

@lru_cache(maxsize=_REQUEST_REFRESH_LIMIT)
def send_subregion_request(subregion: str):
    data = _send_request(host=f'{_COUNTRIES_API_HOST}/subregion/{subregion}')
    return _sanitize_data(data)
