import datetime


def is_event_time():
    e = get_event_times()
    return e[0] or e[1] or e[2]


def get_event_times():
    now = datetime.datetime.now()
    weather_time = now.replace(hour=22, minute=30, second=0, microsecond=0)
    within_weather_time = abs((now - weather_time).total_seconds()) < 10 * 60
    castle_time = now.replace(hour=22, minute=00, second=0, microsecond=0)
    within_castle_time = abs((now - castle_time).total_seconds()) < 10 * 60

    within_new_day = (now.hour == 23 and now.minute > 50) or (now.hour == 0 and now.minute < 10)

    return within_weather_time, within_new_day, within_castle_time