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


def _get_csv_from_qs_values2(queryset: QuerySet[Dict], filename: str = "data"):
    """
    Converts a queryset into a CSV file buffer, including full details of related fields.

    Args:
        queryset (QuerySet): The queryset to export.
        filename (str): The base name of the CSV file.

    Returns:
        io.BytesIO: A buffer containing the CSV file.
    """
    if not queryset.exists():
        raise ValueError("The queryset is empty.")

    # Preparing the complete data for export
    enriched_data = []
    for obj in queryset:
        # Flattening the Movie fields
        movie_data = {key: obj.get(key) for key in obj.keys() if not key.startswith("trailer__")}

        # Flattening the Trailer fields
        if "trailer" in obj:
            trailer_data = {f"trailer_{key}": value for key, value in obj["trailer"].items()}
        else:
            trailer_data = {}

        # Combining Movie and Trailer data
        enriched_data.append({**movie_data, **trailer_data})

    # Extract all unique fieldnames from the enriched data
    fieldnames = set(key for data in enriched_data for key in data.keys())

    # Writing the CSV to a string buffer
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=sorted(fieldnames))
    writer.writeheader()
    writer.writerows(enriched_data)
    csv_buffer.seek(0)

    # Converting to BytesIO for Telegram compatibility
    bytes_buffer = io.BytesIO()
    bytes_buffer.write(csv_buffer.getvalue().encode("utf-8"))
    bytes_buffer.seek(0)
    bytes_buffer.name = f"{filename}__{datetime.now().strftime('%Y.%m.%d.%H.%M')}.csv"

    return bytes_buffer