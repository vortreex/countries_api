"""
This file contains unit tests for functions in csv_converter module.
"""

import src.csv_converter as converter

def test_convert_json_to_csv_when_list_is_given():
    """
    Test for convert_json_to_csv function when JSON data as list is given.
    """
    json_data = [{"name": "Russia", "capital": "Moscow", "region": "Europe", "subregion": "Eastern Europe", "borders": ["AZE", "BLR", "CHN", "EST", "FIN", "GEO", "KAZ", "PRK", "LVA", "LTU", "MNG", "NOR", "POL", "UKR"], "area": 17098242.0, "population": 144104080}, {"name": "Germany", "capital": "Berlin", "region": "Europe", "subregion": "Western Europe", "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"], "area": 357114.0, "population": 83240525},
                 {"name": "France", "capital": "Paris", "region": "Europe", "subregion": "Western Europe", "borders": ["AND", "BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"], "area": 551695.0, "population": 67391582}, {"name": "United Kingdom", "capital": "London", "region": "Europe", "subregion": "Northern Europe", "borders": ["IRL"], "area": 242900.0, "population": 67215293},
                 {"name": "Italy", "capital": "Rome", "region": "Europe", "subregion": "Southern Europe", "borders": ["AUT", "FRA", "SMR", "SVN", "CHE", "VAT"], "area": 301336.0, "population": 59554023},
                 {"name": "Spain", "capital": "Madrid", "region": "Europe", "subregion": "Southern Europe", "borders": ["AND", "FRA", "GIB", "PRT", "MAR"], "area": 505992.0, "population": 47351567},
                 {"name": "Ukraine", "capital": "Kyiv", "region": "Europe", "subregion": "Eastern Europe", "borders": ["BLR", "HUN", "MDA", "POL", "ROU", "RUS", "SVK"], "area": 603500.0, "population": 44134693},
                 {"name": "Poland", "capital": "Warsaw", "region": "Europe", "subregion": "Central Europe", "borders": ["BLR", "CZE", "DEU", "LTU", "RUS", "SVK", "UKR"], "area": 312679.0, "population": 37950802},
                 {"name": "Romania", "capital": "Bucharest", "region": "Europe", "subregion": "Southeast Europe", "borders": ["BGR", "HUN", "MDA", "SRB", "UKR"], "area": 238391.0, "population": 19286123},
                 {"name": "Netherlands", "capital": "Amsterdam", "region": "Europe", "subregion": "Western Europe", "borders": ["BEL", "DEU"], "area": 41850.0, "population": 16655799}]
    expected_csv = 'name,capital,region,subregion,borders,area,population\r\nRussia,Moscow,Europe,Eastern Europe,"[\'AZE\', \'BLR\', \'CHN\', \'EST\', \'FIN\', \'GEO\', \'KAZ\', \'PRK\', \'LVA\', \'LTU\', \'MNG\', \'NOR\', \'POL\', \'UKR\']",17098242.0,144104080\r\nGermany,Berlin,Europe,Western Europe,"[\'AUT\', \'BEL\', \'CZE\', \'DNK\', \'FRA\', \'LUX\', \'NLD\', \'POL\', \'CHE\']",357114.0,83240525\r\nFrance,Paris,Europe,Western Europe,"[\'AND\', \'BEL\', \'DEU\', \'ITA\', \'LUX\', \'MCO\', \'ESP\', \'CHE\']",551695.0,67391582\r\nUnited Kingdom,London,Europe,Northern Europe,[\'IRL\'],242900.0,67215293\r\nItaly,Rome,Europe,Southern Europe,"[\'AUT\', \'FRA\', \'SMR\', \'SVN\', \'CHE\', \'VAT\']",301336.0,59554023\r\nSpain,Madrid,Europe,Southern Europe,"[\'AND\', \'FRA\', \'GIB\', \'PRT\', \'MAR\']",505992.0,47351567\r\nUkraine,Kyiv,Europe,Eastern Europe,"[\'BLR\', \'HUN\', \'MDA\', \'POL\', \'ROU\', \'RUS\', \'SVK\']",603500.0,44134693\r\nPoland,Warsaw,Europe,Central Europe,"[\'BLR\', \'CZE\', \'DEU\', \'LTU\', \'RUS\', \'SVK\', \'UKR\']",312679.0,37950802\r\nRomania,Bucharest,Europe,Southeast Europe,"[\'BGR\', \'HUN\', \'MDA\', \'SRB\', \'UKR\']",238391.0,19286123\r\nNetherlands,Amsterdam,Europe,Western Europe,"[\'BEL\', \'DEU\']",41850.0,16655799\r\n'
    assert converter.convert_json_to_csv(json_data) == expected_csv

def test_convert_json_to_csv_when_dict_is_given():
    """
    Test for convert_json_to_csv function when JSON data as dict is given.
    """

    json_data = {"name": "Russia", "capital": "Moscow", "region": "Europe", "subregion": "Eastern Europe", "borders": ["AZE", "BLR", "CHN", "EST", "FIN", "GEO", "KAZ", "PRK", "LVA", "LTU", "MNG", "NOR", "POL", "UKR"], "area": 17098242.0, "population": 144104080}
    expected_csv = 'name,capital,region,subregion,borders,area,population\r\nRussia,Moscow,Europe,Eastern Europe,"[\'AZE\', \'BLR\', \'CHN\', \'EST\', \'FIN\', \'GEO\', \'KAZ\', \'PRK\', \'LVA\', \'LTU\', \'MNG\', \'NOR\', \'POL\', \'UKR\']",17098242.0,144104080\r\n'

    assert converter.convert_json_to_csv(json_data) == expected_csv
