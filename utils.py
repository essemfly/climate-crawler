import datetime


def get_365_day_interval(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start_date = date_obj.date()
    end_date = start_date + datetime.timedelta(days=364)
    return (start_date, end_date)
