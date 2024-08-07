"""
This module contains integration tests for REST API HTTP server.
"""
from http.server import HTTPServer
from multiprocessing import Process
import requests
import pytest
from src.server import CountriesAPIHandler

_SERVER_LOCAL_IP_ADDR = '127.0.0.5'
_SERVER_LOCAL_PORT_NUMBER = 5005

@pytest.fixture(scope='module')
def server():
    """
    Fixture that starts server before tests and stops it after tests.
    """
    # Start server
    server = HTTPServer((_SERVER_LOCAL_IP_ADDR, _SERVER_LOCAL_PORT_NUMBER), CountriesAPIHandler)
    server_process = Process(target=server.serve_forever, args=())
    server_process.daemon = True
    server_process.start()

    yield

    # Stop server
    server_process.terminate()

def test_top_ten_countries_endpoint_json_header(server) -> None:
    """
    Test checks if server returns correct response for /top_ten_countries endpoint with JSON in header.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/top_ten_countries/Europe', headers={'Accept': 'json'})
    assert response.status_code == 200

    content = response.json()

    assert len(content) == 10

def test_top_ten_countries_endpoint_csv_header(server) -> None:
    """
    Test checks if server returns correct response for /top_ten_countries endpoint with JSON in header.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/top_ten_countries/Europe', headers={'Accept': 'csv'})
    assert response.status_code == 200
    try:
        content = response.json()
    except ValueError:
        content = response.text.rstrip('\n')
    assert len(content.split('\n')) == 11 # 10 countries + header

def test_faulty_endpoint(server) -> None:
    """
    Test checks if server returns correct response for non existing endpoint.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/best_countries_in_that_region/Europe')
    assert response.status_code == 404

    msg = response.text

    assert msg.rstrip('\n') == 'Endpoint not found!'

def test_faulty_param(server) -> None:
    """
    Test checks if server returns correct response for wrong parameter.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/top_ten_countries/Pangea')
    assert response.status_code == 400

    msg = response.text

    assert msg.rstrip('\n') == 'Error retrieving information about contries from remote host'

def test_all_countries_in_subregion(server) -> None:
    """
    Test checks if server returns correct response for /all_countries_in_subregion endpoint.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/all_countries_in_subregion/Western Europe')
    assert response.status_code == 200

    content = response.json()
    for country in content:
        assert country['region'].lower() == 'europe'
        assert country['subregion'].lower() == 'western europe'
        assert len(country['borders']) >= 3

def test_population_of_subregion(server) -> None:
    """
    Test checks if server returns correct response for /population_of_subregion endpoint.
    """

    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/population_of_subregion/Western Europe')
    assert response.status_code == 200
    total_population = 0
    content = response.json()
    for country in content:
        assert country['region'].lower() == 'europe'
        assert country['subregion'].lower() == 'western europe'
        total_population += country['population']

    for country in content:
        assert country['Total subregion population'] == total_population

def test_unsupported_header_type(server) -> None:
    """
    Test checks if server returns correct response for unsupported header type.
    """
    response = requests.get(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/top_ten_countries/Europe', headers={'Accept': 'xml'})
    assert response.status_code == 400

    msg = response.text

    assert msg.rstrip('\n') == 'Accept header must contain either "json" or "csv"'

def test_unsupported_put_request(server) -> None:
    """
    Test checks if server returns correct response for unsupported request type.
    At the moment PUT is not implemented in any way even in errors handling as it is not the part of task.
    """
    response = requests.put(f'http://{_SERVER_LOCAL_IP_ADDR}:{_SERVER_LOCAL_PORT_NUMBER}/top_ten_countries/Europe')
    assert response.status_code == 501