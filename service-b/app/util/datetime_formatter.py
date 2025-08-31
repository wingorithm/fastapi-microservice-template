from datetime import datetime, timezone

import pytz

TRANSACTION_DATE_FORMAT = "%d %b %Y, %H:%M"
DATE_SEGMENT_FORMAT = "%B %Y"

def format_datetime_into_isoformat(date_time: datetime) -> str:
    return date_time.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


"""
Formats a datetime object to transaction date string.

Args:
    date_time (datetime): The datetime object to format

Returns:
    str: Formatted date string (e.g., "24 Mar 2024, 15:30")
"""
def format_transaction_date(date_time: datetime) -> str:
    if not date_time.tzinfo:
        date_time = date_time.replace(tzinfo=pytz.UTC)
    return date_time.strftime(TRANSACTION_DATE_FORMAT) + " WIB"


"""
Formats a datetime object to date segment string.

Args:
    date_time (datetime): The datetime object to format

Returns:
    str: Formatted date string (e.g., "24 March 2024")
"""
def format_date_segment(date_time: datetime) -> str:
    if not date_time.tzinfo:
        date_time = date_time.replace(tzinfo=pytz.UTC)
    return date_time.strftime(DATE_SEGMENT_FORMAT)