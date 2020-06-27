from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
from datetime import datetime as dt
import json

from live.lib.race import get_heat_laps
from live.lib.race import get_last_heat
from live.lib.race import get_heat


def laps_json(request, heat_id=None):
    if heat_id is None:
        heat_id = get_last_heat()
    heat_finished, rtc_time_start, rtc_time_end = get_heat(heat_id)
    heat_duration_seconds = (rtc_time_end - rtc_time_start) / 1000000
    heat_duration = str(timedelta(seconds=heat_duration_seconds))
    data = get_heat_laps(heat_id)
    try:
        heat_start = dt.fromtimestamp(int(rtc_time_start) / 1000000).strftime('%d.%m.%Y  %H:%M')
    except TypeError:
        heat_start = ''
    try:
        heat_end = dt.fromtimestamp(int(rtc_time_end) / 1000000).strftime('%d.%m.%Y  %H:%M')
    except TypeError:
        heat_end = ''
    context = {
            'data': data,
            'heat_id': heat_id,
            'heat_duration': heat_duration,
            'heat_start': heat_start,
            'heat_end': heat_end,
            }
    data = json.dumps(context, indent=4, cls=DjangoJSONEncoder)
    return HttpResponse(data)
