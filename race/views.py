from django.shortcuts import render
from live.lib.race import get_race_data
from live.lib.race import get_last_heat


def heat_by_id(request, heat_id):
    data = get_heat(request, heat_id=heat_id)
    context = {
            'heat_id': heat_id,
            'refresh': False,
            'data': data,
            }
    print(request.content_params)
    return render(request, 'race.html', context)


def heat(request):
    data, heat_id = get_heat(request)
    context = {
            'heat_id': heat_id,
            'refresh': True,
            'data': data,
            }
    print("RACE")
    return render(request, 'race.html', context)


def get_heat(request, heat_id=None):
    if heat_id is None:
        heat_id = get_last_heat()
    print(heat_id)
    data = get_race_data(heat_id)
    print(data)
    return data, heat_id


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
