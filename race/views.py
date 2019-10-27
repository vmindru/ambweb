from django.shortcuts import render
from live.lib.race import get_race_data
from live.lib.race import get_best_lap
from live.lib.race import get_last_heat


def heat_by_id(request, heat_id):
    data, best_lap, heat_id = get_heat(request, heat_id=heat_id)
    context = {
            'heat_id': heat_id,
            'refresh': True,
            'data': data,
            'best_lap': best_lap
            }
    return render(request, 'race.html', context)


def heat(request):
    data, best_lap, heat_id = get_heat(request)
    context = {
            'heat_id': heat_id,
            'refresh': True,
            'data': data,
            'best_lap': best_lap
            }
    return render(request, 'race.html', context)


def get_heat(request, heat_id=None):
    if heat_id is None:
        heat_id = get_last_heat()
    print(heat_id)
    data = get_race_data(heat_id)
    best_lap = get_best_lap(heat_id)
    return data, best_lap, heat_id


def sort_heat(data):
    return dict(sorted(data.items(), key=lambda e: min(e[1]) if len(e[1]) > 0 else 0))


def remove_rtc_time(data):
    for key, values in data.items():
        data[key] = [val[1] for val in values if val[1] > 0]
    return data


def transponder_to_kart_name(dict):
    return dict


def heat_kart(heat_kart):
    pass
