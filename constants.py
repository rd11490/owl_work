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
        (BlizzardWorld, 1): 127.5192413330078,
        (BlizzardWorld, 2): 127.5192413330078,
        (BlizzardWorld, 3): 111.63501739501952,
        (Dorado, 0): 0.0,
        (Dorado, 1): 127.5192413330078,
        (Dorado, 2): 127.5192413330078,
        (Dorado, 3): 111.63501739501952,
        (Eichenwalde, 0): 0.0,
        (Eichenwalde, 1): 127.5192413330078,
        (Eichenwalde, 2): 127.5192413330078,
        (Eichenwalde, 3): 111.63501739501952,
        (Havana, 0): 0.0,
        (Havana, 1): 127.5192413330078,
        (Havana, 2): 127.5192413330078,
        (Havana, 3): 111.63501739501952,
        (Hollywood, 0): 0.0,
        (Hollywood, 1): 127.5192413330078,
        (Hollywood, 2): 127.5192413330078,
        (Hollywood, 3): 111.63501739501952,
        (Junkertown, 0): 0.0,
        (Junkertown, 1): 127.5192413330078,
        (Junkertown, 2): 127.5192413330078,
        (Junkertown, 3): 111.63501739501952,
        (KingsRow, 0): 0.0,
        (KingsRow, 1): 127.5192413330078,
        (KingsRow, 2): 127.5192413330078,
        (KingsRow, 3): 111.63501739501952,
        (Numbani, 0): 0.0,
        (Numbani, 1): 127.5192413330078,
        (Numbani, 2): 127.5192413330078,
        (Numbani, 3): 111.63501739501952,
        (Rialto, 0): 0.0,
        (Rialto, 1): 127.5192413330078,
        (Rialto, 2): 127.5192413330078,
        (Rialto, 3): 111.63501739501952,
        (Route66, 0): 0.0,
        (Route66, 1): 127.5192413330078,
        (Route66, 2): 127.5192413330078,
        (Route66, 3): 111.63501739501952,
        (Gibraltar, 0): 0.0,
        (Gibraltar, 1): 127.5192413330078,
        (Gibraltar, 2): 127.5192413330078,
        (Gibraltar, 3): 111.63501739501952
    }


# TODO Implement OT rules
def time_to_add(map_type, point):
    if map_type == Maps.Assault:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 4 * 60
        elif point % 2 != 0:
            return 30
    if map_type == Maps.Hybrid or map_type == Maps.Escort:
        if point == 0:
            return 4 * 60
        elif point == 1:
            return 2.5 * 60
        elif point == 2:
            return 1.5 * 60
        else:
            return 0

    return 0


def total_map_time(map_type, point):
    total_time = 0
    for i in range(0, point + 1):
        total_time += time_to_add(map_type, i)
    return total_time


def total_escort_map_distance(map_name, point):
    dist = 0.0
    for i in range(0, point + 1):
        if i > 3:
            point_to_check = i % 3
        else:
            point_to_check = i
        dist += Maps.map_dist[(map_name, point_to_check)]
    return dist


hero_pools = [
    {
        'low': '2020/03/06',
        'high': '2020/03/09',
        'pool': 'hero pool 1',
        'bans': ['McCree', 'Widowmaker', 'Reinhardt', 'Moira']
    }, {
        'low': '2020/03/27',
        'high': '2020/03/30',
        'pool': 'hero pool 2',
        'bans': ['Soldier: 76', 'Sombra', 'Winston', 'Lucio']
    }, {
        'low': '2020/04/03',
        'high': '2020/04/07',
        'pool': 'hero pool 3',
        'bans': ['McCree', 'Mei', 'Wrecking Ball', 'Brigitte']
    }, {
        'low': '2020/04/10',
        'high': '2020/04/13',
        'pool': 'hero pool 4',
        'bans': ['Sombra', 'Reaper', 'D.Va', 'Ana']
    }, {
        'low': '2020/04/15',
        'high': '2020/04/20',
        'pool': 'hero pool 5',
        'bans': ['Widowmaker', 'McCree', 'Reinhardt', 'Brigitte']
    }, {
        'low': '2020/04/24',
        'high': '2020/04/27',
        'pool': 'hero pool 6',
        'bans': ['Tracer', 'Echo', 'Orisa', 'Moira']
    }, {
        'low': '2020/05/01',
        'high': '2020/05/04',
        'pool': 'hero pool 7',
        'bans': ['McCree', 'Widowmaker', 'Wrecking Ball', 'Mercy']
    }, {
        'low': '2020/05/08',
        'high': '2020/05/11',
        'pool': 'hero pool 8',
        'bans': ['Ashe', 'Reaper', 'Reinhardt', 'Brigitte']
    }, {
        'low': '2020/05/15',
        'high': '2020/05/18',
        'pool': 'hero pool 9',
        'bans': ['Mei', 'Tracer', 'Orisa', 'Moira']
    }, {
        'low': '2020/05/21',
        'high': '2020/05/25',
        'pool': 'May Melee',
        'bans': []
    }, {
        'low': '2020/06/13',
        'high': '2020/06/22',
        'pool': 'hero pool 10',
        'bans': ['Echo', 'Sombra', 'D.Va', 'Brigitte']
    }, {
        'low': '2020/06/26',
        'high': '2020/07/06',
        'pool': 'Summer Showdown',
        'bans': []
    }, {
        'low': '2020/07/16',
        'high': '2020/07/27',
        'pool': 'hero pool 11',
        'bans': ['Mei', 'Widowmaker', 'Orisa', 'Ana']
    }
]
