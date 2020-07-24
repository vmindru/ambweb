from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import json

from live.lib.race import get_race_data
from live.lib.race import get_best_lap
from live.lib.race import get_last_heat
from live.lib.race import get_heat


def live_json(request, heat_id=None):
    def get_index(val):
        return data_header.index(val)
    data, best_lap, heat_id, heat_finished, rtc_time_start, rtc_time_end = get_live_data(request, heat_id=heat_id)
    heat_duration_seconds = (rtc_time_end - rtc_time_start) / 1000000
    heat_duration = str(timedelta(seconds=heat_duration_seconds))
    try:
        heat_start = dt.fromtimestamp(int(rtc_time_start) / 1000000).strftime('%d.%m.%Y  %H:%M')
    except TypeError:
        heat_start = ''
    try:
        heat_end = dt.fromtimestamp(int(rtc_time_end) / 1000000).strftime('%d.%m.%Y  %H:%M')
    except TypeError:
        heat_end = ''

    """ we need to replace transponder from last colum from SQL query dataset
    with values from best_lap before sneding to render"""
    data = list(data)
    data_header = ['Position', 'Kart', 'Name', 'Laps', 'Lap Time', 'Raced Time', 'Average', 'Diff', 'Best Lap Time', 'Best Lap']
    for index, value in enumerate(data):
        position = index + 1  # set Kart Position
        value = list(value)
        transponder_id = value[6]
        best_heat_lap_time = min([item[0] for item in best_lap.values()])
        best_lap_time = list(best_lap[transponder_id])
        value.insert(0, position)
        laps_count = value[get_index('Laps')]
        raced_time = value[get_index('Raced Time')]
        diff = round(best_lap_time[0] - best_heat_lap_time, 3)
        t = dt.combine(date.min, raced_time) - dt.min
        raced_seconds = t.total_seconds()
        value[get_index('Diff')] = diff
        lap_time_avg = round(raced_seconds / laps_count, 3)
        print(lap_time_avg)
        print(diff)
        value[get_index('Average')] = lap_time_avg
        data[index] = value + best_lap_time
    context = {
            'data': data,
            'heat_id': heat_id,
            'heat_duration': heat_duration,
            'heat_start': heat_start,
            'heat_end': heat_end,
            }
    d = context
    data = json.dumps(d, indent=4, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def get_live_data(request, heat_id=None):
    if heat_id is None:
        heat_id = get_last_heat()
    heat_finished, rtc_time_start, rtc_time_end = get_heat(heat_id)
    data = get_race_data(heat_id)
    best_lap = get_best_lap(heat_id)
    return data, best_lap, heat_id, heat_finished, rtc_time_start, rtc_time_end
