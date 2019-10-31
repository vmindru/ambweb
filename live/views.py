from django.shortcuts import render
from live.lib.race import get_amb_data
from live.lib.race import get_last_heat
from pprint import pprint

def heat_id(request, heat_id):
    data, laps, heat_id, karts_dict = get_heat(request, heat_id=heat_id)
    context = {
            'data': data,
            'laps': laps,
            'heat_id': heat_id,
            'refresh': False,
            'kart_dict': karts_dict,
            }
    print(request.content_params)
    return render(request, 'live.html', context)

def heat(request):
    data, laps, heat_id, karts_dict = get_heat(request)
    context = {
            'data': data,
            'laps': laps,
            'heat_id': heat_id,
            'refresh': True,
            'kart_dict': karts_dict,
            }
    return render(request, 'live.html', context)


def get_heat(request, heat_id=None):
    refresh = True

    if heat_id is None:
        heat_id = get_last_heat()

    heat = get_amb_data(heat_id=heat_id)
    data = sort_heat(remove_rtc_time(transponder_to_kart_name(heat.dict)))
    laps = range(0, heat.get_number_of_laps())
    karts_dict = heat.kart_ids
    return data, laps, heat_id, karts_dict


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
