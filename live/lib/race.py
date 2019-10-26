from live.models import Laps
from live.models import Heats
from live.models import Karts
from django.db import connections


def get_amb_data(heat_id):
    heat = Heat(heat_id)
    for transponder_id in get_heat_transponders(heat_id):
        for rtc_time in get_transponder_laps(heat_id, transponder_id):
            heat.add_pass(transponder_id, rtc_time)
    return heat


class Heat():
    def __init__(self, heat_id):
        self.id = heat_id
        self.dict = {}
        self.kart_ids = kart_ids(Karts.objects.values('kart_number', 'transponder_id'))

    def add_pass(self, transponder_id,  rtc_time):
        if transponder_id not in self.dict:
            self.dict[transponder_id] = [(rtc_time, 0)]
        else:
            prev_time = self.dict[transponder_id][-1][0]
            lap_time = (rtc_time - prev_time) / 1000000
            self.dict[transponder_id].append((rtc_time, lap_time))

    def get_number_of_laps(self):
        return max([len(laps) for laps in self.dict.values()])


def get_race_data(heat_id):
    select_query = "select karts.kart_number,t5.laps_count,t5.lap_time from ( select t2.transponder_id,\
laps_count,((t2.rtc_time - t3.rtc_time) / 1000000 ) as lap_time  from\
( select transponder_id , rtc_time from laps as t1 where rtc_time=(select  max(rtc_time) from laps where \
transponder_id=t1.transponder_id and heat_id={heat_id} ) ) as t2  join ( select transponder_id , rtc_time from laps as \
t1 where rtc_time=(select rtc_time from laps where transponder_id=t1.transponder_id and heat_id={heat_id} order by \
pass_id desc  limit 1 offset 1  )) as t3 join ( select transponder_id,count(*) as laps_count from laps where \
heat_id={heat_id}  group  by transponder_id  ) as t4  on t2.transponder_id=t4.transponder_id and \
t4.transponder_id=t3.transponder_id  order by t4.laps_count desc) as t5 join karts on t5.transponder_id = \
karts.transponder_id".format(heat_id=heat_id)
    with connections['kartsdb'].cursor() as cursor:
        cursor.execute(select_query)
        res = cursor.fetchall()
    return res


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
