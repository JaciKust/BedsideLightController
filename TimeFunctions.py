import datetime


def get_next(of_time, from_datetime=None):
    if from_datetime is None:
        from_datetime = datetime.datetime.now()

    new_date = from_datetime
    if from_datetime.time() >= of_time:
        new_date = from_datetime + datetime.timedelta(days=1)

    return datetime.datetime.combine(new_date, of_time)

