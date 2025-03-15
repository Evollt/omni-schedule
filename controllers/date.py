from datetime import datetime
import pytz

class Date:
    def get_start_and_end_time(date, time):
        # Предположим, что это время в вашем локальном часовом поясе (например, Москва)
        local_tz = pytz.timezone('Europe/Moscow')

        # Преобразование времени в локальном часовом поясе в UTC
        time_local = local_tz.localize(datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M'))

        time_utc = time_local.astimezone(pytz.utc).strftime('%Y%m%dT%H%M00Z')

        return time_utc