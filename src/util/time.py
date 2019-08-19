from datetime import datetime, timedelta

from pytz import utc


def from_unix_timestamp(ts):
    """ Returns a UTC DateTime from a unix timestamp. """
    return datetime.utcfromtimestamp(ts).replace(tzinfo=utc)


def to_unix_timestamp(dt):
    """ Returns an integer unix timestamp representing the give DateTime. """
    return (dt - datetime.fromtimestamp(0, dt.tzinfo)).total_seconds()


def to_unix_timestamp_millis(dt):
    return to_unix_timestamp(dt) * 1000.0


def now():
    """ Returns current datetime as UTC. """
    return datetime.utcnow().replace(tzinfo=utc)


def ago(**kwargs):
    """
    Returns UTC datetime for some timedelta ago.
    Ex: ago(days=1, hours=4)  # UTC DateTime for 1 day, 4 hours ago.
    """
    return now() - timedelta(**kwargs)


def floor_to_minute(dt):
    """ Returns dt floored to minute. """
    return dt.replace(second=0, microsecond=0)


def floor_to_hour(dt):
    """ Returns dt floored to hour. """
    return dt.replace(minute=0, second=0, microsecond=0)


def floor_to_day(dt):
    """ Returns dt floored to day. """
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def floor_to_month(dt):
    """ Returns dt floored to month. """
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def floor_to_year(dt):
    """ Returns dt floored to year. """
    return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def ceil_to_minute(dt):
    """ Returns dt ceiled to minute. """
    if floor_to_minute(dt) == dt:
        return dt
    return floor_to_minute(floor_to_minute(dt) + timedelta(seconds=61))


def ceil_to_hour(dt):
    """ Returns dt ceiled to hour. """
    if floor_to_hour(dt) == dt:
        return dt
    return floor_to_hour(floor_to_hour(dt) + timedelta(minutes=61))


def ceil_to_day(dt):
    """ Returns dt ceiled to day. """
    if floor_to_day(dt) == dt:
        return dt
    return floor_to_day(floor_to_day(dt) + timedelta(hours=25))


def ceil_to_month(dt):
    """ Returns dt ceiled to month. """
    if floor_to_month(dt) == dt:
        return dt
    return floor_to_month(floor_to_month(dt) + timedelta(days=32))


def ceil_to_year(dt):
    """ Returns dt ceiled to year. """
    if floor_to_year(dt) == dt:
        return dt
    return floor_to_year(floor_to_year(dt) + timedelta(days=366))


def seconds(num):
    """ Returns timedelta representing num minutes. """
    return timedelta(seconds=num)


def minutes(num):
    """ Returns timedelta representing num minutes. """
    return timedelta(minutes=num)


def hours(num):
    """ Returns timedelta representing num hours. """
    return timedelta(hours=num)


def days(num):
    """ Returns timedelta representing num days. """
    return timedelta(days=num)
