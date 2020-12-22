"""
Some functions about date and time
"""
from datetime import date, datetime  # Taqvim Miladi
from jdatetime import datetime as jdatetime  # Taqvim Shamsi


def get_delta_time(input_date) -> str:
    """
    Calculates the delta of local time with inputed date

    :return -> Only delta of dates, it ignores the clock
    """
    inputed_date = str(input_date.split("T")[0]).split("-")
    year = inputed_date[0]
    month = inputed_date[1]
    day = inputed_date[2]

    first_date = date(int(year), int(month), int(day))
    local_date = date.today()
    return str(local_date - first_date).split(",")[0]


def get_date() -> dict:
    """
    Gets today month and day in Miladi & Shamsi from your local timezone

    :returns -> Miladi & Shamsi month-day in a dict
    """
    today = datetime.now()
    j_today = jdatetime.now()
    return {
        'month': str(today.strftime("%B")), 'day': str(today.day),
        'jmonth': str(j_today.strftime("%B")), 'jday': str(j_today.day)}


def get_time() -> dict:
    """
    Gets local time by hour and minuts from your local timezone

    :return -> hour:minute in dictionery
    """
    local_time = datetime.now()
    return {'hours': local_time.hour, 'minutes': local_time.minute}
