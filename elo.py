import pandas as pd
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

frame = pd.read_csv('data/match_map_stats.csv')

teams = frame['attacker'].unique()
maps = frame['map_name'].unique()


class MapType:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    map_types = {
        'Hanamura': Assault,
        'Horizon Lunar Colony': Assault,
        'Paris': Assault,
        'Temple of Anubis': Assault,
        'Volskaya Industries': Assault,

        'Busan': Control,
        'Ilios': Control,
        'Lijiang Tower': Control,
        'Nepal': Control,
        'Oasis': Control,

        'Dorado': Escort,
        'Havana': Escort,
        'Junkertown': Escort,
        'Rialto': Escort,
        'Route 66': Escort,
        'Watchpoint: Gibraltar': Escort,

        'Numbani': Hybrid,
        'Eichenwalde': Hybrid,
        "King's Row": Hybrid,
        'Hollywood': Hybrid,
        'Blizzard World': Hybrid,
    }


def calc_map_type(map_name):
    return MapType.map_types[map_name]


def calc_match_date(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y/%m/%d")


def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y")


def calculate_control_winner(row):
    if row['attacker_control_perecent'] == 100.0:
        return row['attacker']
    else:
        return row['defender']


def calculate_control_loser(row):
    if row['attacker_control_perecent'] == 100.0:
        return row['defender']
    else:
        return row['attacker']


frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)

escort_maps = frame[frame['map_type'] == MapType.Escort]
assault_maps = frame[frame['map_type'] == MapType.Assault]
control_maps = frame[frame['map_type'] == MapType.Control]
hybrid_maps = frame[frame['map_type'] == MapType.Hybrid]

escort_maps = escort_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'winning_team_final_map_score',
     'losing_team_final_map_score', 'match_date', 'season']].drop_duplicates()
assault_maps = assault_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'match_date', 'season']].drop_duplicates()
control_maps = control_maps[
    ['map_name', 'control_round_name', 'team_one_name', 'team_two_name', 'match_date', 'attacker', 'defender', 'attacker_control_perecent',
     'defender_control_perecent', 'season']].drop_duplicates()
control_maps['map_winner'] = control_maps.apply(calculate_control_winner, axis=1)
control_maps['map_loser'] = control_maps.apply(calculate_control_loser, axis=1)

hybrid_maps = hybrid_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'match_date', 'season']].drop_duplicates()


def update_elo(elo, winner, team1, team2):
    elo1 = elo[team1]
    elo2 = elo[team2]

    r1 = 10 ** (elo1 / 400)
    r2 = 10 ** (elo2 / 400)
    e1 = r1 / (r1 + r2)
    e2 = r2 / (r1 + r2)

    if winner == 'draw':
        s1 = 0.5
        s2 = 0.5
    elif winner == team1:
        s1 = 1.0
        s2 = 0.0
    else:
        s1 = 0.0
        s2 = 1.0

    elo[team1] = elo1 + 50 * (s1-e1)
    elo[team2] = elo2 + 50 * (s2-e2)


def decay_elo(teams_elo):
    for team in teams:
        diff = teams_elo[team] - 1500
        regress = diff * 0.25
        teams_elo[team] -= regress
    return teams_elo


def calculate_elo(frame):
    elo = {}
    for team in teams:
        elo[team] = 1500

    curr_season = frame.loc[frame.index[0], :]['season']
    for i in frame.index:

        if frame.loc[i, :]['season'] != curr_season:
            elo = decay_elo(elo)
            curr_season = frame.loc[i, :]['season']

        update_elo(elo, frame.loc[i, :]['map_winner'], frame.loc[i, :]['team_one_name'],
                   frame.loc[i, :]['team_two_name'])

    elo = {k: v for k, v in sorted(elo.items(), key=lambda item: item[1], reverse=True)}
    elo = pd.DataFrame([ {'Team': k, 'Elo': v } for k, v in elo.items()])
    return elo


escort_elo = calculate_elo(escort_maps)
print('ESCORT MAP ELO')
print(escort_elo)
print('\n')



control_elo = calculate_elo(control_maps)
print('CONTROL MAP ELO')
print(control_elo)
print('\n')


assault_elo = calculate_elo(assault_maps)
print('ASSAULT MAP ELO')
print(assault_elo)
print('\n')


hybrid_elo = calculate_elo(hybrid_maps)
print('HYBRID MAP ELO')
print(hybrid_elo)
print('\n')


