from django.shortcuts import render
from live.lib.race import get_amb_data
from live.lib.race import get_last_heat


def index(request):
    heat_id = get_last_heat()
    heat = get_amb_data(heat_id=heat_id)
    data = heat.dict
    for key, values in data.items():
        data[key] = [val[1] for val in values if val[1] > 0]
    laps = range(0, heat.get_number_of_laps())
    return render(request, 'index.html', {'data': data, 'laps': laps })
