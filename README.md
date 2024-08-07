# Countries API

## Introduction
This is the Countries API service. This repository contains modules that allows to run a server which retrieves information about countries from remote host and offers three endpoint with which it provides it in more feasbile way

# Usage

In order to use this service you'll need environment with installed Python (version 3.10 and onwards were tested, version 3.9 should also run without problems, but bare minimum is Python version 3.6, due to usage of f-strings) or Docker.

To run server in docker container simply use:

> docker compose up

The first execution will be slower due to process of building the image from Dockerfile, but each next usage should be faster.

Or you can build the image on your own and run it with commands:

>docker build -t countries-api .
>
>docker run -p <*local_ip_addres*>:<*port_number*>:80 countries-api

With Python interpreter, firstly you have to add project to $PYTHONPATH. The easiest way is to go to project directory and execute given command:

>export PYTHONPATH=\`pwd\`

After that step simply run server.py file:

> python3 src/server.py

Great, now you have running server that responds to HTTP request.
Here are the endpoints it supports:

  - **/top_ten_countries/{region}** - responds with list of the 10 biggest countries of a determined region of the world (Europe, Asia, Oceania, Americas, etc). When sending request {region} should be substituted with the name of the region we want to have information about.
  - **/all_countries_in_subregion/{region}** - responds with list of all the countries of a determined subregion (South America, West Europe,  Eastern Asia, etc) that has borders with more than 3 countries. When sending request {subregion} should be substituted with the name of the subregion we want to have information about.
 - **/population_of_subregion/{subregion}** - responds with list of all the countries of a determined subregion (South America, West Europe,  Eastern Asia, etc) and attaches information about total population of subregion to information about each country (for convenience of CSV format). When sending request {subregion} should be substituted with the name of the subregion we want to have information about.

The server supports response represented in two formats: **JSON** and **CSV**!

You can retrieve information from given endpoints with different tools. Here are the examples of using cURL python library 'requests'.

### cURL
Install cURL with any package manager you have and send GET requests with given command:
> curl -X GET -H "Accept: application/<*json*/*csv*>" <*ip_address*>:<*port_number*>/top_ten_countries/Asia

For example:

> curl -X GET -H "Accept: application/json" 127.0.0.1:80/top_ten_countries/Asia

> curl -X GET -H "Accept: application/csv" 127.0.0.1:80/all_countries_in_subregion/Western%20Asia

>curl -X GET 127.0.0.1:80/population_of_subregion/Central%20Europe

Remember, when specifing region or subregion name that contains spaces, change spaces to "%20" in order for cURL to correctly determine endpoint.

### Python
With Python and requests module installed simply run requests.get() function!

For example:

> import requests
>
> response = requests.get(f'http://127.0.0.1:80/population_of_subregion/Western Europe')

> import requests
>
> response = response = requests.get(f'http://127.0.0.1:80/top_ten_countries/Europe', headers={'Accept': 'csv'})


## Documentation
This part of the documentation covers all the interfaces of Countries API. Its classes, methods, functions, constants required parameters and theirs type as well as return objects in order to explain it so you can alter the behaviour of the program in any suitable way.

### server.py

This module contains definition of class representing server for Countries API.

class server.**CountriesAPIHandler**

Class representing handler for server for Countries API.

#### **do_GET**()

Function that handles HTTP GET requests received by the server.
  
  **Raises**:
  - **ValueError** - If the header or processed request contains unsupported response format (other than JSON or CSV)

#### **_ten_biggest_countries_by_region**(*region*, *csv_output*)

Function that handles endpoint /top_ten_countries/{region}
  
  **Parameters**:
  - **region** (*str*) - Region name
  - **csv_coutput** (*bool*) - Set to true of data should be in CSV format, JSON otherwise

#### **_all_countries_in_subregion**(*subregion*, *csv_output*)

Function that handles endpoint /all_countries_in_subregion/{region}
  
  **Parameters**:
  - **subregion** (*str*) - Subregion name
  - **csv_coutput** (*bool*) - Set to true of data should be in CSV format, JSON otherwise

#### **_population_of_subregion**(*subregion*, *csv_output*)

Function that handles endpoint /population_of_subregion/{subregion}
  
  **Parameters**:
  - **subregion** (*str*) - Subregion name
  - **csv_coutput** (*bool*) - Set to true of data should be in CSV format, JSON otherwise

#### **_parse_path**()

Function that parses path from request and retrieves parameter value.
  
  **Returns**: Tuple containing path and parameter.

#### **_set_response_type**()

Function that checks what type of response should be sent. If JSON is requested, it returns False, if CSV is requested, it returns True. If both JSON and CSV are requested, JSON is selected. If no header is present, JSON is selected.
  
**Returns**: True if only CSV is requested, False otherwise

#### **_convert_data_to_requested_type**(*data*, *csv_output*)

Function that converts data to requested type.
  
  **Parameters**:
  - **data** (*dict | list*) - Data to be converted.
  - **csv_coutput** (*bool*) - Flag indicating if only CSV output is requested.

  **Returns**: Converted data.

#### **_send_response**(*message*, *status_code*)

Function that sends response to client.
  
  **Parameters**:
  - **message** (*str*) - Message to be sent.
  - **status_code** (*int*) - Status code of the response.

#### Constants
  Behaviour of this module is defined with some constant value that can be changed in order to achieve different goals.
  - **_MINIMAL_NEIGHBOURS_NUMBER** = 3 - specifies the minimal number of neighbours that country needs to be included in the response from /all_countries_in_subregion/{region} endpoint.
  - **_BIGGEST_COUNTRIES_IN_REGION_LIMIT** = 10 - specifies the number of countries included in response from /top_ten_countries/{region}
  - **_OK_STATUS_CODE** = 200 - status code indicating correct request and no errors when processing the request.
  - **_NOK_STATUS_CODE** = 400 - status code indicating error with endpoint parameter or errors when processing the request.
  - **_RESOURCE_NOT_FOUND_STATUS_CODE** = 404 - status code indicating that request was sent to not existing endpoint
  - **_COUNTRY_SIZE_DEF** = 'population' - definition of metric which is used to determine biggest countries. 'area' can be used instead.
  - **_REMOTE_HOST_ERROR_MSG** = 'Error retrieving information about contries from remote host' - message sent when there are issues with connection to remote host.
  - **_RESOURCE_NOT_FOUND_MSG** = 'Endpoint not found!' - message sent when request was sent to nonexisting endpoint.
  - **_BAD_HEADER_TYPE_MSG** = 'Accept header must contain either "json" or "csv"' - message sent when request contains not supported response format in header.
  - **_EMPTY_HEADERS** = ('/\*/', '\*/\*', '') - tuple of string that represent empty header. Different programs for sending HTTP request can format empty headers in different way. In order to adjust to it this tuple should be expanded.

### Data consumer (data_consumer.py)

This module contains function to convert JSON-like objects (dicts and lists) to CSV files.

#### **send_region_request**(*region*)

  Function that sends REST API request to remote host in order to retrieve data about countries in specified region and caches it.
  
  **Parameters**:
  - **region** (*str*) - Region name

  **Returns**: List of dictionaries containing information about countries in region

#### **send_subregion_request**(*subregion*)

  Function that sends REST API request to remote host in order to retrieve data about countries in specified region and caches it.
  
  **Parameters**:
  - **subregion** (*str*) - Subregion name

  **Returns**: List of dictionaries containing information about countries in subregion

#### **_sanitize_data**(*data*)

Function that sanitizes retrieved data by removing redundant country names and flattens single element lists. The index error may occure as some countries might not have specified capital. This function can be modified to achieve different representation of information.
  
  **Parameters**:
  - **data** (*list*) - Unsanitized data

  **Returns**: Sanitized data

  **Raises**:
  - **IndexError** - May occure if country has not specified field (i.e. capital)

#### **_send_request**(*host*)

    Function that handles sending the request to remote API Host.
  
  **Parameters**:
  - **host** (*str*) - Remote API Host URL

  **Returns**: JSON like object (dictionary or list) containing retrieved data.
    
  **Raises**:
  - **requests.exceptions.ConnectionError** - If the host is not reachable.
  - **requests.exceptions.HTTPError** - If the status code of the response from remote host is not in the OK range (200 - 300)

#### Constants
  Behaviour of this module is defined with some constant value that can be changed in order to achieve different goals.
  - **_REQUEST_TIMEOUT** = 10 - specifies time in second after which it considers request to not be processed
  - **_CACHE_CAPACITY** = 5 - specifies the capacity of the cache i.e. how many different function calls result can be stored
  - **_COUNTRIES_API_HOST** = https://restcountries.com/v3.1 - specifies remote API host from which data is retrieved.
  - **_COUNTRY_PARAMS** = {'fields': ['name','capital', 'region', 'subregion','population', 'area', 'borders']} - specifies parameters for HTTP GET request to remote host. In this case it filters interesting countries' information. 

### CSV Converter (csv_converter.py)

This module contains function to convert JSON-like objects (dicts and lists) to CSV files.

#### **convert_json_to_csv**(*data*)

  Function that converts JSON-like object to CSV file.
  
  **Parameters**:
  - **data** (*dict | list*) - JSON-like object to be converted

  **Returns**: Data in CSV format as string.

#### Constants
  Behaviour of this module is defined with some constant value that can be changed in order to achieve different goals.
  - **_CSV_DIALECT** = 'excel' - specifies which CSV format is being used
  - **_MISSING_VAL** = "-" - specifies what value will be put if converter considers field to be empty.

### Tests
The "test" folder contains unit and integration tests for provided server. You can verify the correct behaviour of this service by running those tests with Python's pytest module.

For example:
> \>pytest test/unit/*

> \>cd test/integration
>
> \>pytest test_server.py
