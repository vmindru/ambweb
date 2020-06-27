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


def get_best_lap(heat_id):
    heat = Heat(heat_id)
    for transponder_id in get_heat_transponders(heat_id):
        for rtc_time in get_transponder_laps(heat_id, transponder_id):
            heat.add_pass(transponder_id, rtc_time)
    heat_dict = heat.dict
    for key, value in heat_dict.items():
        if len(value) > 1:
            lap_times = [item[1] for item in value]
            best_lap_time = min(lap_times[1:])
            best_lap = lap_times.index(best_lap_time)
            heat_dict[key] = (best_lap_time, best_lap)
        else:
            heat_dict[key] = (0, 0)
    return heat_dict


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


def get_heat_laps(heat_id):
    #    drop_query = "DROP TABLE current_heat;"
    create_query = f"CREATE temporary table if not exists current_heat as \
( select *  from laps where heat_id={heat_id});"
#    get_karts_query = f"select  name  from  ( select DISTINCT transponder_id from laps where heat_id={heat_id})\
#  as t left join karts on t.transponder_id=karts.transponder_id"
    select_query = """
SELECT TRUNCATE(lap_time / 1000000,3),kart_number from (
SELECT
  heatA.pass_id, heatA.transponder_id,
  COALESCE(heatA.rtc_time - HeatB.rtc_time, 0) AS lap_time
FROM
  current_heat    AS heatA
LEFT JOIN
  current_heat    AS HeatB
    ON  HeatB.transponder_id   = heatA.transponder_id
    AND HeatB.pass_id = (SELECT MAX(pass_id)
                          FROM current_heat
                         WHERE transponder_id = heatA.transponder_id
                           AND pass_id < heatA.pass_id) ) as heat left join karts
                                   on heat.transponder_id = karts.transponder_id
                           order by kart_number,pass_id ;
"""
    with connections['kartsdb'].cursor() as cursor:
        cursor.execute(create_query)
        cursor.execute(select_query)
        data = cursor.fetchall()
    laps = {}
    for entry in data:
        if entry[1] not in laps:
            laps[entry[1]] = []
        elif entry[0] > 0:
            laps[entry[1]].append(entry[0])
    data = dict(sorted(laps.items(), key=lambda kv: kv[1]))
    laps = list(zip(*list(data.values())))
#    header = [{"title": str(item)} for item in list(data.keys())]
    header = list(data.keys())
    return header, laps


def get_race_data(heat_id):
    select_query = """
SELECT ifnull(karts.kart_number, t5.transponder_id),
       t5.laps_count,
       t5.lap_time,
       sec_to_time((t5.time_raced / 1000000)) AS time_raced,
       (t5.time_raced) AS seconds_raced,
       ifnull(karts.transponder_id, t5.transponder_id)
FROM
  (SELECT t2.transponder_id,
          laps_count,
          ((t2.rtc_time - t3.rtc_time) / 1000000) AS lap_time,
          (t2.rtc_time -
             (SELECT rtc_time_start
              FROM heats
              WHERE heat_id={0} )) AS time_raced
   FROM
     (SELECT transponder_id,
             rtc_time
      FROM laps AS t1
      WHERE rtc_time=
          (SELECT max(rtc_time)
           FROM laps
           WHERE transponder_id=t1.transponder_id
             AND heat_id={0} ) ) AS t2
   JOIN
     (SELECT transponder_id,
             rtc_time
      FROM laps AS t1
      WHERE rtc_time=
          (SELECT rtc_time
           FROM laps
           WHERE transponder_id=t1.transponder_id
             AND heat_id={0}
           ORDER BY pass_id DESC
           LIMIT 1
           OFFSET 1)) AS t3
   JOIN
     (SELECT transponder_id,
             count(*) -1 AS laps_count
      FROM laps
      WHERE heat_id={0} GROUP  BY transponder_id ) AS t4 ON t2.transponder_id=t4.transponder_id
   AND t4.transponder_id=t3.transponder_id) AS t5
LEFT JOIN karts ON t5.transponder_id = karts.transponder_id
ORDER BY t5.laps_count DESC, t5.time_raced""".format(heat_id)

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


def get_heat(heat_id):
    heat_finished = Heats(heat_id=heat_id).heat_finished
    rtc_time_start = Heats.objects.get(heat_id=heat_id).rtc_time_start
    rtc_time_end = Heats.objects.get(heat_id=heat_id).rtc_time_end
    # print(rtc_time_start, rtc_time_end)
    return heat_finished, rtc_time_start, rtc_time_end
