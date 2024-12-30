import io
import csv

from datetime import datetime
from django.db.models import QuerySet
from typing import Dict


def _get_csv_from_qs_values(queryset: QuerySet[Dict], filename: str = 'users'):
    keys = queryset[0].keys()

    # csv module can write data in io.StringIO buffer only
    s = io.StringIO()
    dict_writer = csv.DictWriter(s, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(queryset)
    s.seek(0)

    # python-telegram-bot library can send files only from io.BytesIO buffer
    # we need to convert StringIO to BytesIO
    buf = io.BytesIO()

    # extract csv-string, convert it to bytes and write to buffer
    buf.write(s.getvalue().encode())
    buf.seek(0)

    # set a filename with file's extension
    buf.name = f"{filename}__{datetime.now().strftime('%Y.%m.%d.%H.%M')}.csv"

    return buf


import csv
import io
from typing import Dict
from datetime import datetime
from django.db.models import QuerySet


def _get_csv_from_qs_values2(queryset: QuerySet[Dict], filename: str = "data"):
    """
    Converts a queryset into a CSV file buffer, including details from related fields.

    Args:
        queryset (QuerySet): The queryset to export.
        filename (str): The base name of the CSV file.

    Returns:
        io.BytesIO: A buffer containing the CSV file.
    """
    if not queryset.exists():
        raise ValueError("The queryset is empty.")

    # Extract field names from the first object in the queryset
    fieldnames = set()
    for item in queryset:
        fieldnames.update(item.keys())

    # Writing the CSV data to a StringIO buffer
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=sorted(fieldnames))
    writer.writeheader()
    writer.writerows(queryset)
    csv_buffer.seek(0)

    # Convert to BytesIO for Telegram compatibility
    bytes_buffer = io.BytesIO()
    bytes_buffer.write(csv_buffer.getvalue().encode("utf-8"))
    bytes_buffer.seek(0)
    bytes_buffer.name = f"{filename}__{datetime.now().strftime('%Y.%m.%d.%H.%M')}.csv"

    return bytes_buffer