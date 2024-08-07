"""
This module contains function to convert JSON-like objects (dicts and lists) to CSV files.
"""
import io
import csv

_CSV_DIALECT = "excel"
_MISSING_VAL = "-"


def convert_json_to_csv(data: dict | list) -> str:
    """
    Function that converts JSON-like object to CSV file.
    :param data: JSON-like object to be converted
    :param filename: Name of the file to be created
    """
    if isinstance(data, dict):
        data = [data]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys(), dialect=_CSV_DIALECT,
                            restval=_MISSING_VAL, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)

    return output.getvalue()
