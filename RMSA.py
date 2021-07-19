import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)

pd.set_option('display.width', 1000)


player_rows = pd.read_csv('results/map_lineups.csv')
map_scores = pd.read_csv('results/scored_maps.csv')

map_scores_swapped = map_scores.copy(deep=True)
map_scores_swapped['team_one_name'] = map_scores['team_two_name']
map_scores_swapped['team_two_name'] = map_scores['team_one_name']
map_scores_swapped['team_one_score'] = map_scores['team_two_score']
map_scores_swapped['team_two_score'] = map_scores['team_one_score']


map_scores = pd.concat([map_scores, map_scores_swapped])


map_scores = map_scores[map_scores['season'] == 2020]

joined = map_scores.merge(player_rows, how='left', left_on=['match_id', 'map_name', 'team_one_name'],
                          right_on=['match_id', 'map_name', 'team']).merge(player_rows, how='left',
                                                                           left_on=['match_id', 'map_name',
                                                                                    'team_two_name'],
                                                                           right_on=['match_id', 'map_name', 'team'])

joined.columns = ['match_id', 'game_number', 'map_name', 'map_winner', 'match_date',
                  'team_one_name', 'team_two_name', 'team_one_score',  'team_two_score', 'season','team_one', 'p1_team_one',
                  'p2_team_one', 'p3_team_one', 'p4_team_one', 'p5_team_one', 'p6_team_one', 'team_two', 'p1_team_two',
                  'p2_team_two', 'p3_team_two', 'p4_team_two', 'p5_team_two', 'p6_team_two']

joined['Net Score'] = (joined['team_one_score'] - joined['team_two_score'])/2.0

joined = joined[['Net Score', 'p1_team_one', 'p2_team_one', 'p3_team_one', 'p4_team_one', 'p5_team_one', 'p6_team_one',
                 'p1_team_two', 'p2_team_two', 'p3_team_two', 'p4_team_two', 'p5_team_two', 'p6_team_two']]

joined = joined.dropna()


# 'p1_team_one', 'p2_team_one', 'p3_team_one', 'p4_team_one', 'p5_team_one', 'p6_team_one', 'p1_team_two', 'p2_team_two', 'p3_team_two', 'p4_team_two', 'p5_team_two', 'p6_team_two']
players = list(set(list(joined['p1_team_one'].values) + \
           list(joined['p2_team_one'].values) + \
           list(joined['p3_team_one'].values) + \
           list(joined['p4_team_one'].values) + \
           list(joined['p5_team_one'].values) + \
           list(joined['p6_team_one'].values) + \
           list(joined['p1_team_two'].values) + \
           list(joined['p2_team_two'].values) + \
           list(joined['p3_team_two'].values) + \
           list(joined['p4_team_two'].values) + \
           list(joined['p5_team_two'].values) + \
           list(joined['p6_team_two'].values)))
players = [str(p) for p in players]
players = sorted(players)

def map_players(row_in, players):
    p1 = row_in[0]
    p2 = row_in[1]
    p3 = row_in[2]
    p4 = row_in[3]
    p5 = row_in[4]
    p6 = row_in[5]
    p7 = row_in[6]
    p8 = row_in[7]
    p9 = row_in[8]
    p10 = row_in[9]
    p11 = row_in[10]
    p12 = row_in[11]


    row_out = np.zeros([len(players)])

    row_out[players.index(p1)] = 1
    row_out[players.index(p2)] = 1
    row_out[players.index(p3)] = 1
    row_out[players.index(p4)] = 1
    row_out[players.index(p5)] = 1
    row_out[players.index(p6)] = 1

    row_out[players.index(p7)] = -1
    row_out[players.index(p8)] = -1
    row_out[players.index(p9)] = -1
    row_out[players.index(p10)] = -1
    row_out[players.index(p11)] = -1
    row_out[players.index(p12)] = -1

    return row_out

print(joined)

stints_x_base = joined.as_matrix(columns=['p1_team_one', 'p2_team_one', 'p3_team_one', 'p4_team_one', 'p5_team_one', 'p6_team_one',
                 'p1_team_two', 'p2_team_two', 'p3_team_two', 'p4_team_two', 'p5_team_two', 'p6_team_two'])

stint_X_rows = np.apply_along_axis(map_players, 1, stints_x_base, players)

stint_Y_rows = joined.as_matrix(['Net Score'])
# Convert lambda value to alpha needed for ridge CV
def lambda_to_alpha(lambda_value, samples):
    return (lambda_value * samples) / 2.0


# Convert RidgeCV alpha back into a lambda value
def alpha_to_lambda(alpha_value, samples):
    return (alpha_value * 2.0) / samples

lambdas = [.01, 0.025, .05, 0.075, .1, .125, .15, .175, .2, .225, .25]


alphas = [lambda_to_alpha(l, stint_X_rows.shape[0]) for l in lambdas]

clf = RidgeCV(alphas=alphas, cv=5, fit_intercept=True, normalize=False)

model = clf.fit(stint_X_rows, stint_Y_rows)

player_arr = np.transpose(np.array(players).reshape(1, len(players)))
coef_array = np.transpose(model.coef_)

player_id_with_coef = np.concatenate([player_arr, coef_array], axis=1)
# build a dataframe from our matrix
rmsa = pd.DataFrame(player_id_with_coef)
intercept = model.intercept_

rmsa.columns = ['player', 'RMSA']
rmsa['RMSA'] = rmsa['RMSA'].astype(float)
rmsa = rmsa.sort_values(by='RMSA', ascending=False)
print(rmsa.head(1000))
print(intercept)



rmsa.to_csv('results/rmsa.csv', index=False)