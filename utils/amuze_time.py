import datetime

TIME_FORMAT_1 = "%H:%M:%S.%f"
TIME_FORMAT_2 = "%H:%M:%S"
SECONDS_IN_ONE_HOUR = 3600
SECONDS_IN_ONE_MINUTE = 60


def convert_time_str_to_seconds(time_str):
    try:
        tmp = datetime.datetime.strptime(time_str, TIME_FORMAT_1).time()
    except Exception:
        tmp = datetime.datetime.strptime(time_str, TIME_FORMAT_2).time()
    return tmp.hour * SECONDS_IN_ONE_HOUR + tmp.minute * SECONDS_IN_ONE_MINUTE + tmp.second


def convert_seconds_to_time_str(seconds):
    hours = int(seconds / SECONDS_IN_ONE_HOUR)
    minutes = int((seconds % SECONDS_IN_ONE_HOUR) / SECONDS_IN_ONE_MINUTE)
    seconds %= SECONDS_IN_ONE_MINUTE
    tmp_time = datetime.time(hour=hours, minute=minutes, second=seconds)
    return tmp_time.strftime("%H:%M:%S")
