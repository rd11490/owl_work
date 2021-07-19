

class Maps:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    Hanamura = 'Hanamura'
    HorizonLunarColony = 'Horizon Lunar Colony'
    Paris = 'Paris'
    TempleOfAnubis = 'Temple of Anubis'
    VolskayaIndustries = 'Volskaya Industries'
    Busan = 'Busan'
    Ilios = 'Ilios'
    LijiangTower = 'Lijiang Tower'
    Nepal = 'Nepal'
    Oasis = 'Oasis'
    Dorado = 'Dorado'
    Havana = 'Havana'
    Junkertown = 'Junkertown'
    Rialto = 'Rialto'
    Route66 = 'Route 66'
    Gibraltar = 'Watchpoint: Gibraltar'
    Numbani = 'Numbani'
    Eichenwalde = 'Eichenwalde'
    KingsRow = 'King\'s Row'
    Hollywood = 'Hollywood'
    BlizzardWorld = 'Blizzard World'

    map_types = {
        Hanamura: Assault,
        HorizonLunarColony: Assault,
        Paris: Assault,
        TempleOfAnubis: Assault,
        VolskayaIndustries: Assault,

        Busan: Control,
        Ilios: Control,
        LijiangTower: Control,
        Nepal: Control,
        Oasis: Control,

        Dorado: Escort,
        Havana: Escort,
        Junkertown: Escort,
        Rialto: Escort,
        Route66: Escort,
        Gibraltar: Escort,

        Numbani: Hybrid,
        Eichenwalde: Hybrid,
        KingsRow: Hybrid,
        Hollywood: Hybrid,
        BlizzardWorld: Hybrid,
    }

    # Hybrid maps first point distance is given the distance from point 1-2
    map_dist = {
        (BlizzardWorld, 0): 0.0,
        (BlizzardWorld, 1): 127.0,
        (BlizzardWorld, 2): 127.51924129999999,
        (BlizzardWorld, 3): 127.5221481,
        (Dorado, 0): 0.0,
        (Dorado, 1): 85.32969666,
        (Dorado, 2): 96.17001343,
        (Dorado, 3): 96.18503571,
        (Eichenwalde, 0): 0.0,
        (Eichenwalde, 1): 127.0,
        (Eichenwalde, 2): 127.75437930000001,
        (Eichenwalde, 3): 127.7602997,
        (Havana, 0): 0.0,
        (Havana, 1): 88.14551544,
        (Havana, 2): 91.14924622,
        (Havana, 3): 102.2647095,
        (Hollywood, 0): 0.0,
        (Hollywood, 1): 119.0,
        (Hollywood, 2): 119.06569669999999,
        (Hollywood, 3): 119.0059967,
        (Junkertown, 0): 0.0,
        (Junkertown, 1): 89.97218323,
        (Junkertown, 2): 89.98745728,
        (Junkertown, 3): 101.8506012,
        (KingsRow, 0): 0.0,
        (KingsRow, 1): 114.0,
        (KingsRow, 2): 114.52094270000002,
        (KingsRow, 3): 112.87974550000001,
        (Numbani, 0): 0.0,
        (Numbani, 1): 96.0,
        (Numbani, 2): 96.78807831,
        (Numbani, 3): 95.84685516,
        (Rialto, 0): 0.0,
        (Rialto, 1): 97.04573059,
        (Rialto, 2): 103.72267149999999,
        (Rialto, 3): 103.26073459999999,
        (Route66, 0): 0.0,
        (Route66, 1): 83.64376831,
        (Route66, 2): 90.58800507,
        (Route66, 3): 89.54434204,
        (Gibraltar, 0): 0.0,
        (Gibraltar, 1): 85.99927521,
        (Gibraltar, 2): 85.80711365,
        (Gibraltar, 3): 88.13453674
    }

# TODO Implement OT rules
def time_to_add(mapType, point):
    if mapType == Maps.Assault:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 4 * 60
        elif point % 2 != 0:
            return 30
    if mapType == Maps.Hybrid or mapType == Maps.Escort:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 3 * 60
        elif point == 2:
            return 2 * 60
        else:
            return 0
    else:
        return 0

def total_map_time(mapType, point):
    total_time = 0
    for i in range(0, point+1):
        total_time += time_to_add(mapType, i)
    return total_time

def total_escort_map_distance(map, point):
    dist = 0.0
    for i in range(0, point+1):
        if i > 3:
            point_to_check = i%3
        else:
            point_to_check = i
        dist += Maps.map_dist[(map, point_to_check)]
    return dist



hero_pools = [
    {
        'low': '2020/03/06',
        'high': '2020/03/09',
        'pool': 'hero pool 1',
        'bans': ['McCree', 'Widowmaker', 'Reinhardt', 'Moira']
     },{
        'low': '2020/03/27',
        'high': '2020/03/30',
        'pool': 'hero pool 2',
        'bans': ['Soldier: 76', 'Sombra', 'Winston', 'Lucio']
     },{
        'low': '2020/04/03',
        'high': '2020/04/07',
        'pool': 'hero pool 3',
        'bans': ['McCree', 'Mei', 'Wrecking Ball', 'Brigitte']
     },{
        'low': '2020/04/10',
        'high': '2020/04/13',
        'pool': 'hero pool 4',
        'bans': ['Sombra', 'Reaper', 'D.Va', 'Ana']
     },{
        'low': '2020/04/15',
        'high': '2020/04/20',
        'pool': 'hero pool 5',
        'bans': ['Widowmaker', 'McCree', 'Reinhardt', 'Brigitte']
     },{
        'low': '2020/04/24',
        'high': '2020/04/27',
        'pool': 'hero pool 6',
        'bans': ['Tracer', 'Echo','Orisa', 'Moira']
     },{
        'low': '2020/05/01',
        'high': '2020/05/04',
        'pool': 'hero pool 7',
        'bans': ['McCree', 'Widowmaker', 'Wrecking Ball', 'Mercy']
     },{
        'low': '2020/05/08',
        'high': '2020/05/11',
        'pool': 'hero pool 8',
        'bans': ['Ashe', 'Reaper', 'Reinhardt', 'Brigitte']
     },{
        'low': '2020/05/15',
        'high': '2020/05/18',
        'pool': 'hero pool 9',
        'bans': ['Mei', 'Tracer', 'Orisa', 'Moira']
     },{
        'low': '2020/05/21',
        'high': '2020/05/25',
        'pool': 'May Melee',
        'bans': []
     },{
        'low': '2020/06/13',
        'high': '2020/06/22',
        'pool': 'hero pool 10',
        'bans': ['Echo', 'Sombra', 'D.Va', 'Brigitte']
     },{
        'low': '2020/06/26',
        'high': '2020/07/06',
        'pool': 'Summer Showdown',
        'bans': []
     },{
        'low': '2020/07/16',
        'high': '2020/07/27',
        'pool': 'hero pool 11',
        'bans': ['Mei', 'Widowmaker', 'Orisa', 'Ana']
     }
]