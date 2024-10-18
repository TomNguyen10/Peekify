from datetime import datetime, timedelta


def get_date_range_for_last_week():
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday(), weeks=1)
    last_monday = last_monday.replace(
        hour=0, minute=0, second=0, microsecond=0)
    last_sunday = last_monday + \
        timedelta(days=6, hours=23, minutes=59, seconds=59)
    return last_monday, last_sunday


def get_most_recent_monday():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)
