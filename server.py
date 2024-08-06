from copy import deepcopy
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from requests import HTTPError
from data_consumer import send_region_request, send_subregion_request

_MINIMAL_NEIGHBOURS_NUMBER = 3
_BIGGEST_COUNTRIES_IN_REGION_LIMIT = 10
_OK_STATUS_CODE = 200
_NOK_STATUS_CODE = 400
_RESOURCE_NOT_FOUND_STATUS_CODE = 404
_COUNTRY_SIZE_DEFINITION = 'population'  # can be changed to 'area' for example
_REMOTE_HOST_ERROR_MSG = 'Error retrieving information about contries from remote host'
_RESOURCE_NOT_FOUND_MSG = 'Endpoint not found!'

class CountriesAPIServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path, param = self._parse_path()
        match path:
            case '/top_ten_countries':
                self._ten_biggest_countries_by_region(region=param)
            case '/all_countries_in_subregion':
                self._all_countries_in_subregion(subregion=param)
            case '/population_of_subregion':
                self._population_of_subregion(subregion=param)
            case _:
                self._send_response(message=_RESOURCE_NOT_FOUND_MSG, status_code=_RESOURCE_NOT_FOUND_STATUS_CODE)
        
    def _ten_biggest_countries_by_region(self, region: str = None):
        try:
            data = data = send_region_request(region=region)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return
        
        data = sorted(data, reverse=True, key=lambda x: x[_COUNTRY_SIZE_DEFINITION])[:_BIGGEST_COUNTRIES_IN_REGION_LIMIT]
        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _all_countries_in_subregion(self, subregion: str = None):
        try:
            data = send_subregion_request(subregion=subregion)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return

        data = [country for country in data if len(country['borders']) > _MINIMAL_NEIGHBOURS_NUMBER]
        data = json.dumps(data)
        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _population_of_subregion(self, subregion: str = None):
        try:
            data = send_subregion_request(subregion=subregion)
        except HTTPError:
            self._send_response(message=_REMOTE_HOST_ERROR_MSG, status_code=_NOK_STATUS_CODE)
            return
        
        subregion_population = sum([country['population'] for country in data])
        data = [country | {'Total subregion population': subregion_population} for country in data]
        data = json.dumps(data)
        self._send_response(message=data, status_code=_OK_STATUS_CODE)

    def _parse_path(self):
        param = self.path.rstrip('/').split('/')[-1].replace('%20', ' ').lower()
        path = '/'.join(self.path.rstrip('/').split('/')[:-1])
        return path, param

    def _send_response(self, message: str, status_code: int):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(f'{message}\n'.encode())


if __name__ == "__main__":    
    httpd = HTTPServer(('127.0.0.1', 2137), CountriesAPIServer)
    httpd.serve_forever()
