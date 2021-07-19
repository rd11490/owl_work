import pandas as pd
import datetime
import matplotlib.pyplot as plt
from utils import calc_match_date, calc_season


from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

frame = pd.read_csv('map_data/match_map_stats.csv')

teams = frame['attacker'].unique()
maps = frame['map_name'].unique()


###
# Preprocessor helper functions
###

def calc_map_type(map_name):
    return Maps.map_types[map_name]





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



###
# Process data
###

frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)

escort_maps = frame[frame['map_type'] == Maps.Escort]
assault_maps = frame[frame['map_type'] == Maps.Assault]
control_maps = frame[frame['map_type'] == Maps.Control]
hybrid_maps = frame[frame['map_type'] == Maps.Hybrid]

escort_maps = escort_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'winning_team_final_map_score',
     'losing_team_final_map_score', 'match_date', 'season']].drop_duplicates()
assault_maps = assault_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'match_date', 'season']].drop_duplicates()
control_maps = control_maps[
    ['map_name', 'control_round_name', 'team_one_name', 'team_two_name', 'match_date', 'attacker', 'defender', 'attacker_control_perecent',
     'defender_control_perecent', 'season']].drop_duplicates()

control_maps['map_name'] = control_maps['map_name'] + ' - ' + control_maps['control_round_name']
control_maps['map_winner'] = control_maps.apply(calculate_control_winner, axis=1)
control_maps['map_loser'] = control_maps.apply(calculate_control_loser, axis=1)

hybrid_maps = hybrid_maps[
    ['map_winner', 'map_loser', 'team_one_name', 'team_two_name', 'map_name', 'match_date', 'season']].drop_duplicates()




####
# Let's test K
####

###
# Calculate Elo
###

class EloCalculator:

    def __init__(self, k = 20, base_elo = 1500, season_reset=0.5):
        self.k = k
        self.base_elo = base_elo
        self.season_reset = season_reset


    def __update_elo(self, elo, winner, team1, team2):
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

        err1 = s1-e1
        err2 = s2-e2
        elo[team1] = elo1 + self.k * err1
        elo[team2] = elo2 + self.k * err2

        return err2**2 + err1**2


    def __decay_elo(self, teams_elo):
        for team in teams:
            new_elo = teams_elo[team] * self.season_reset + self.base_elo * (1.0-self.season_reset)
            teams_elo[team] = new_elo
        return teams_elo


    def calculate_elo(self, frame):
        error = 0.0
        elo = {}
        for team in teams:
            elo[team] = self.base_elo

        curr_season = frame.loc[frame.index[0], :]['season']
        for i in frame.index:
            if frame.loc[i, :]['season'] != curr_season:
                elo = self.__decay_elo(elo)
                curr_season = frame.loc[i, :]['season']

            error += self.__update_elo(elo, frame.loc[i, :]['map_winner'], frame.loc[i, :]['team_one_name'],
                   frame.loc[i, :]['team_two_name'])

        elo_map = {k: v for k, v in sorted(elo.items(), key=lambda item: item[1], reverse=True)}
        elo = pd.DataFrame([ {'Team': k, 'Elo': v } for k, v in elo_map.items()])
        return elo, elo_map, error



all_maps = pd.concat([
    escort_maps[['map_winner', 'team_one_name', 'team_two_name', 'map_name','season', 'match_date']],
    hybrid_maps[['map_winner', 'team_one_name', 'team_two_name', 'map_name', 'season', 'match_date']],
    control_maps[['map_winner', 'team_one_name', 'team_two_name', 'map_name', 'season', 'match_date']],
    assault_maps[['map_winner', 'team_one_name', 'team_two_name', 'map_name', 'season', 'match_date']],
])

print(all_maps)

train = all_maps[all_maps['match_date'] < '2020/06/13']
test = all_maps[all_maps['match_date'] >= '2020/06/13']



# ks = []
# errors = []
#
# for k in range(0, 100):
#     print(k)
#     elo_model = EloCalculator(k=k, base_elo=1500)
#     map_elo = {}
#     error = 0
#     maps_group = all_maps.groupby('map_name')
#     for m in maps_group:
#         elo, err = elo_model.calculate_elo(m[1])
#         map_elo[m[0]] = elo
#         error += err
#     ks.append(k)
#     errors.append(error)
#
# plt.plot(ks, errors)
# plt.show()

elo_model = EloCalculator(k=75, base_elo=1500, season_reset=0.5)
map_elo = {}
error = 0
maps_group = train.groupby('map_name')
for m in maps_group:
    elo, elo_map, err = elo_model.calculate_elo(m[1])
    map_elo[m[0]] = elo_map
    error += err


expected_team_one = []
expected_team_two = []

for i in test.index:
    team1 = test.loc[i, :]['team_one_name']
    team2 = test.loc[i, :]['team_two_name']
    map = test.loc[i, :]['map_name']

    elo1 = map_elo[map][team1]
    elo2 = map_elo[map][team2]

    r1 = 10 ** (elo1 / 400)
    r2 = 10 ** (elo2 / 400)
    e1 = r1 / (r1 + r2)
    e2 = r2 / (r1 + r2)

    expected_team_one.append(e1)
    expected_team_two.append(e2)

test['team_one_expected'] = expected_team_one
test['team_two_expected'] = expected_team_two
test['team_one_actual'] = (test['map_winner'] == test['team_one_name']).astype('float')
test['team_two_actual'] = (test['map_winner'] == test['team_two_name']).astype('float')


print(test)


