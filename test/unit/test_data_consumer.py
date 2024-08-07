"""
This file contains unit tests for functions in data_consumer module.
"""
import requests
import src.data_consumer as consumer

def test_send_region_request():
    """
    Test for send_region_request function.
    """
    mock_data = [{'name': 'New Caledonia', 'capital': 'Nouméa', 'region': 'Oceania', 'subregion': 'Melanesia', 'borders': [], 'area': 18575.0, 'population': 271960},
                 {'name': 'Solomon Islands', 'capital': 'Honiara', 'region': 'Oceania', 'subregion': 'Melanesia', 'borders': [], 'area': 28896.0, 'population': 686878},
                 {'name': 'Marshall Islands', 'capital': 'Majuro', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 181.0, 'population': 59194},
                 {'name': 'Vanuatu', 'capital': 'Port Vila', 'region': 'Oceania', 'subregion': 'Melanesia', 'borders': [], 'area': 12189.0, 'population': 307150},
                 {'name': 'Niue', 'capital': 'Alofi', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 260.0, 'population': 1470},
                 {'name': 'Nauru', 'capital': 'Yaren', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 21.0, 'population': 10834},
                 {'name': 'Cocos (Keeling) Islands', 'capital': 'West Island', 'region': 'Oceania', 'subregion': 'Australia and New Zealand', 'borders': [], 'area': 14.0, 'population': 544},
                 {'name': 'Fiji', 'capital': 'Suva', 'region': 'Oceania', 'subregion': 'Melanesia', 'borders': [], 'area': 18272.0, 'population': 896444},
                 {'name': 'Wallis and Futuna', 'capital': 'Mata-Utu', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 142.0, 'population': 11750},
                 {'name': 'Cook Islands', 'capital': 'Avarua', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 236.0, 'population': 18100},
                 {'name': 'Australia', 'capital': 'Canberra', 'region': 'Oceania', 'subregion': 'Australia and New Zealand', 'borders': [], 'area': 7692024.0, 'population': 25687041},
                 {'name': 'Tuvalu', 'capital': 'Funafuti', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 26.0, 'population': 11792},
                 {'name': 'Pitcairn Islands', 'capital': 'Adamstown', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 47.0, 'population': 56},
                 {'name': 'Christmas Island', 'capital': 'Flying Fish Cove', 'region': 'Oceania', 'subregion': 'Australia and New Zealand', 'borders': [], 'area': 135.0, 'population': 2072},
                 {'name': 'Guam', 'capital': 'Hagåtña', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 549.0, 'population': 168783},
                 {'name': 'Tonga', 'capital': "Nuku'alofa", 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 747.0, 'population': 105697},
                 {'name': 'Tokelau', 'capital': 'Fakaofo', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 12.0, 'population': 1411},
                 {'name': 'Samoa', 'capital': 'Apia', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 2842.0, 'population': 198410},
                 {'name': 'Kiribati', 'capital': 'South Tarawa', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 811.0, 'population': 119446},
                 {'name': 'French Polynesia', 'capital': 'Papeetē', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 4167.0, 'population': 280904},
                 {'name': 'Papua New Guinea', 'capital': 'Port Moresby', 'region': 'Oceania', 'subregion': 'Melanesia', 'borders': ['IDN'], 'area': 462840.0, 'population': 8947027},
                 {'name': 'Palau', 'capital': 'Ngerulmud', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 459.0, 'population': 18092},
                 {'name': 'American Samoa', 'capital': 'Pago Pago', 'region': 'Oceania', 'subregion': 'Polynesia', 'borders': [], 'area': 199.0, 'population': 55197},
                 {'name': 'Northern Mariana Islands', 'capital': 'Saipan', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 464.0, 'population': 57557},
                 {'name': 'Norfolk Island', 'capital': 'Kingston', 'region': 'Oceania', 'subregion': 'Australia and New Zealand', 'borders': [], 'area': 36.0, 'population': 2302},
                 {'name': 'New Zealand', 'capital': 'Wellington', 'region': 'Oceania', 'subregion': 'Australia and New Zealand', 'borders': [], 'area': 270467.0, 'population': 5084300},
                 {'name': 'Micronesia', 'capital': 'Palikir', 'region': 'Oceania', 'subregion': 'Micronesia', 'borders': [], 'area': 702.0, 'population': 115021}]

    assert  consumer.send_region_request('Oceania') == mock_data

def test_send_region_request_faulty():
    """
    Test for send_region request function with faulty region.
    """
    try:
        response = consumer.send_region_request('GargBAAAAGE')
    except requests.exceptions.HTTPError:
        assert True
    else:
        assert False, f'Expected HTTPError, got {response}'

def test_send_subregion_request():
    """
    Test for send_subregion_request function.
    """
    mock_data = [{"name": "Hungary", "capital": "Budapest", "region": "Europe", "subregion": "Central Europe", "borders": ["AUT", "HRV", "ROU", "SRB", "SVK", "SVN", "UKR"], "area": 93028.0, "population": 9749763},
                 {"name": "Slovakia", "capital": "Bratislava", "region": "Europe", "subregion": "Central Europe", "borders": ["AUT", "CZE", "HUN", "POL", "UKR"], "area": 49037.0, "population": 5458827},
                 {"name": "Poland", "capital": "Warsaw", "region": "Europe", "subregion": "Central Europe", "borders": ["BLR", "CZE", "DEU", "LTU", "RUS", "SVK", "UKR"], "area": 312679.0, "population": 37950802},
                 {"name": "Slovenia", "capital": "Ljubljana", "region": "Europe", "subregion": "Central Europe", "borders": ["AUT", "HRV", "ITA", "HUN"], "area": 20273.0, "population": 2100126},
                 {"name": "Austria", "capital": "Vienna", "region": "Europe", "subregion": "Central Europe", "borders": ["CZE", "DEU", "HUN", "ITA", "LIE", "SVK", "SVN", "CHE"], "area": 83871.0, "population": 8917205},
                 {"name": "Czechia", "capital": "Prague", "region": "Europe", "subregion": "Central Europe", "borders": ["AUT", "DEU", "POL", "SVK"], "area": 78865.0, "population": 10698896}]

    assert  consumer.send_subregion_request('Central Europe') == mock_data

def test_send_subregion_request_faulty():
    """
    Test for send subregion request function with faulty subregion.
    """
    try:
        response = consumer.send_subregion_request('random garbage')
    except requests.exceptions.HTTPError:
        assert True
    else:
        assert False, f'Expected HTTPError, got {response}'

def test__send_request():
    """
    Test for _send_request function.
    """
    response = consumer._send_request(host='https://restcountries.com/v3.1/region/Oceania')
    assert isinstance(response, list)
    assert len(response) > 0

def test__send_request_faulty():
    """
    Test for _send_request function with faulty API host.
    """
    try:
        response = consumer._send_request(host='https://restcountries.com/v3.1/region/nasdfhjkadgxhjfgasdjhgfhjksdg')
    except requests.exceptions.HTTPError:
        assert True
    else:
        assert False, f'Expected HTTPError, got {response}'

def test__sanitize_data():
    """
    Test for _sanitize_data function.
    """

    sanitized_mock_data = [{"name": "Poland", "capital": "Warsaw", "region": "Europe", "subregion": "Central Europe", "borders": ["BLR", "CZE", "DEU", "LTU", "RUS", "SVK", "UKR"], "area": 312679.0, "population": 37950802}]

    raw_mock_data = [{"name":{"common":"Poland","official":"Republic of Poland","nativeName":{"pol":{"official":"Rzeczpospolita Polska","common":"Polska"}}},"capital":["Warsaw"],"region":"Europe","subregion":"Central Europe","borders":["BLR","CZE","DEU","LTU","RUS","SVK","UKR"],"area":312679.0,"population":37950802}]

    assert consumer._sanitize_data(raw_mock_data) == sanitized_mock_data
