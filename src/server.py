"""
This module contains definition of class representing server for Countries API.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from requests import HTTPError
from src.csv_converter import convert_json_to_csv
from src.data_consumer import send_region_request, send_subregion_request

_MINIMAL_NEIGHBOURS_NUMBER = 3
_BIGGEST_COUNTRIES_IN_REGION_LIMIT = 10
_OK_STATUS_CODE = 200
_NOK_STATUS_CODE = 400
_RESOURCE_NOT_FOUND_STATUS_CODE = 404
_COUNTRY_SIZE_DEF = 'population'  # can be changed to 'area' for example
_REMOTE_HOST_ERROR_MSG = 'Error retrieving information about contries from remote host'
_RESOURCE_NOT_FOUND_MSG = 'Endpoint not found!'
_BAD_HEADER_TYPE_MSG = 'Accept header must contain either "json" or "csv"'
_EMPTY_HEADERS = ('/*/', '*/*', '')

class CountriesAPIHandler(BaseHTTPRequestHandler):
    """
    Class representing handler for server for Countries API.
    """
    def do_GET(self) -> None:
        """
        Function that handles HTTP GET requests received by the server.
        """
        path, param = self._parse_path()
        try:
            csv_output = self._set_response_type()
        except ValueError:
            self._send_response(message=_BAD_HEADER_TYPE_MSG, status_code=_NOK_STATUS_CODE)
            return

        match path:
            case '/top_ten_countries':
                self._ten_biggest_countries_by_region(region=param, csv_output=csv_output)
            case '/all_countries_in_subregion':
                self._all_countries_in_subregion(subregion=param, csv_output=csv_output)
            case '/population_of_subregion':
                self._population_of_subregion(subregion=param, csv_output=csv_output)
            case _:
                self._send_response(message=_RESOURCE_NOT_FOUND_MSG,
                                    status_code=_RESOURCE_NOT_FOUND_STATUS_CODE)

    def _ten_biggest_countries_by_region(self, region: str = None, csv_output: bool = False) -> None:
        """
        Function that handles endpoint /top_ten_countries/{region}
        :param region: Region name
        """
        try:
            data = data = send_region_request(region=region)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return

        data = sorted(data, reverse=True,
                      key=lambda x: x[_COUNTRY_SIZE_DEF])[:_BIGGEST_COUNTRIES_IN_REGION_LIMIT]

        data = self._convert_data_to_requested_type(data=data, csv_output=csv_output)

        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _all_countries_in_subregion(self, subregion: str = None, csv_output: bool = False) -> None:
        """
        Function that handles endpoint /all_countries_in_subregion/{region}
        :param subregion: Subregion name
        """
        try:
            data = send_subregion_request(subregion=subregion)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return

        data = [country for country in data if len(country['borders']) > _MINIMAL_NEIGHBOURS_NUMBER]

        data = self._convert_data_to_requested_type(data=data, csv_output=csv_output)

        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _population_of_subregion(self, subregion: str = None, csv_output: bool = False) -> None:
        """
        Function that handles endpoint /population_of_subregion/{subregion}
        :param subregion: Subregion name
        """
        try:
            data = send_subregion_request(subregion=subregion)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return

        subregion_population = sum([country['population'] for country in data])
        data = [country | {'Total subregion population': subregion_population} for country in data]

        data = self._convert_data_to_requested_type(data=data, csv_output=csv_output)

        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _parse_path(self) -> tuple[str, str]:
        """
        Function that parses path from request.
        :return: Tuple containing path and parameter.
        """
        param = self.path.rstrip('/').split('/')[-1].replace('%20', ' ').lower()
        path = '/'.join(self.path.rstrip('/').split('/')[:-1])
        return path, param

    def _set_response_type(self) -> bool:
        """
        Function that checks wht type of response should be sent.
        If JSON is requested, it returns False, if CSV is requested, it returns True.
        If both JSON and CSV are requested, JSON is returned.
        If no header is present, JSON is returned.
        :return: True if only CSV is requested, False otherwise.
        """
        header_accept_info = self.headers.get('Accept')
        print(header_accept_info)
        if 'json' in header_accept_info or header_accept_info in _EMPTY_HEADERS:
            return False

        if 'csv' in header_accept_info:
            return True

        raise ValueError('Accept header must contain either "json" or "csv"')

    def _convert_data_to_requested_type(self, data: dict | list, csv_output: bool) -> str | list:
        """
        Function that converts data to requested type.
        :param data: Data to be converted.
        :param csv_output: Flag indicating if only CSV output is requested.
        :return: Converted data.
        """
        if csv_output:
            return convert_json_to_csv(data=data)

        return json.dumps(data)

    def _send_response(self, message: str, status_code: int) -> None:
        """
        Function that sends response to client.
        :param message: Message to be sent.
        :param status_code: Status code of the response.
        """
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(f'{message}\n'.encode())


if __name__ == "__main__":
    httpd = HTTPServer(('127.0.0.1', 2137), CountriesAPIHandler)
    httpd.serve_forever()
    httpd.serve
