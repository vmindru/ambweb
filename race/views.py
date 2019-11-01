from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime as dt
from datetime import time
import json


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


def heat_refresh(request):
    return render(request, 'ref.html')


def heat_json(request):
    def get_index(val):
        return data_header.index(val)
    data, best_lap, heat_id = get_heat(request)
    """ we need to replace transponder from last colum from SQL query dataset
    with values from best_lap before sneding to render"""
    data = list(data)
    data_header = ['Position','Kart','Laps', 'Lap Time', 'Raced Time', 'Diff', 'Gap', 'Best Lap Time', 'Best Lap']
    for index, value in enumerate(data):
        position = index + 1  # set Kart Position
        value = list(value)
        best_lap_time_data = list(best_lap[value[5]])
        value.insert(0,position)
        print(value)
        """ calculate Diff to next Kart """
        if index == 0:
            prev_value = value
        if index > 0:
            """ if in the same LAP  diff , else print number of laps DIFF """
            lap_count = value[get_index('Laps')]
            prev_position_lap_count = prev_value[get_index('Laps')]
            leader_lap_count = data[0][get_index('Laps')]
            raced_time = value[get_index('Raced Time')]
            prev_position_raced_time = prev_value[get_index('Raced Time')]
            leader_raced_time = data[0][get_index('Raced Time')]
            raced_seconds = ( dt.combine(dt.min, raced_time))
            prev_position_raced_seconds = ( dt.combine(dt.min, prev_position_raced_time))
            leader_raced_seconds = ( dt.combine(dt.min, leader_raced_time))
            diff_laps = "{} Laps".format(lap_count - prev_position_lap_count)
            gap_laps = "{} Laps".format(lap_count - leader_lap_count)

            if lap_count == prev_position_lap_count:
                diff = round((raced_seconds - prev_position_raced_seconds).total_seconds(),3)
            else:
                diff = diff_laps

            if lap_count == leader_lap_count:
                gap = round((raced_seconds - leader_raced_seconds).total_seconds(),3)
            elif lap_count == prev_position_lap_count:
                gap = 0
                for rev_index in range(index-1,-1,-1):
                    prev_diff = data[rev_index][5]
                    if not isinstance(prev_diff, str):
                        gap = round((prev_diff + gap),3)
                        print(diff)
                    else:
                        gap = prev_diff
                        print("String: {}".format(diff))
                        break
            else:
                gap = gap_laps

            value[5] = diff
            value[6] = gap
            prev_value = value

        else:
            "assign diff and gap, and assign prev_value for next run"
            value[5] = 0
            value[6] = 0
            prev_value = value

        data[index] = value + best_lap_time_data
    context = {
            'heat_id': heat_id,
            'refresh': True,
            'data': data,
            'data_header': data_header,
            }
    d = context
    data = json.dumps(d, indent=4, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def get_heat(request, heat_id=None):
    if heat_id is None:
        heat_id = get_last_heat()
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
