from live.models import Laps
from live.models import Heats
from live.models import Karts


class Heat():
    def __init__(self, heat_id):
        self.id = heat_id
        self.dict = {}
        self.kart_ids = kart_ids(Karts.objects.values('kart_number','transponder_id'))

    def add_pass(self, transponder_id,  rtc_time):
        if transponder_id not in self.dict:
            self.dict[transponder_id] = [(rtc_time, 0)]
        else:
            prev_time = self.dict[transponder_id][-1][0]
            lap_time = (rtc_time - prev_time) / 1000000
            self.dict[transponder_id].append((rtc_time, lap_time))

    def get_number_of_laps(self):
        return max([len(laps) for laps in self.dict.values()])


def get_amb_data(heat_id):
    heat = Heat(heat_id)
    for transponder_id in get_heat_transponders(heat_id):
        for rtc_time in get_transponder_laps(heat_id, transponder_id):
            heat.add_pass(transponder_id, rtc_time)
    return heat


def get_heat_transponders(heat_id):
    transponders = Laps.objects.filter(heat_id=heat_id).values('transponder_id').distinct()
    trlist = [transponder['transponder_id'] for transponder in transponders]
    return trlist


def get_transponder_laps(heat_id, transponder_id):
    """ get passes for transponder_id during heat_id"""
    res = Laps.objects.filter(heat_id=heat_id).filter(transponder_id=transponder_id).order_by('pass_id')
    res = [each.rtc_time for each in res]
    return res


def get_last_heat():
    return Heats.objects.last().heat_id

def kart_ids(QuerySet):
    karts = {}
    for entry in QuerySet:
        karts[entry['transponder_id']] = entry['kart_number']
    return karts

def get_kart_ids(transponder_id, transponder_kart_dict):
    if transponder_id in transponder_kart_dict():
        return transponder_kart_dict[transponder_id]
    else:
        return transponder_id




