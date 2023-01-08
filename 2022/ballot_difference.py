
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

ballots = pd.read_csv('ballots.csv')

winners = ['Hanbin', 'Reiner', 'Smurf', 'Hadi', 'Chiyo', 'Fielder', 'Shu', 'Izayaki', 'Proper', 'Lip', 'Profit', 'Kevster']

print(ballots)

ballots_for_counts = ballots[['Tank1', 'Tank2', 'Tank3', 'Tank4', 'Sup1', 'Sup2', 'Sup3', 'Sup4', 'DPS1', 'DPS2', 'DPS3', 'DPS4']]

voters = ballots_for_counts.shape[0]

votes = []
for c in ballots_for_counts.columns:
    votes = votes + list(ballots_for_counts[c].values)

frame = pd.DataFrame()
frame['player'] = votes
frame['vote'] = 1
counts = frame.groupby('player').sum().reset_index()
counts['pct'] = counts['vote'] / voters
counts = counts.set_index('player')
score_map = counts.to_dict('index')

ballot_items = ballots.to_dict('records')
scores = []

def calc_score(item, role):
    score = 0
    for i in range(1,5):
        vote = item[f'{role}{i}']
        score += score_map[vote]['pct']
    return score

for item in ballot_items:
    dps_score =calc_score(item, 'DPS')
    sup_score =calc_score(item, 'Sup')
    tank_score =calc_score(item, 'Tank')
    total_score = dps_score + sup_score + tank_score
    scores.append({
        'Name': item['Name'],
        'Support': sup_score,
        'DPS': dps_score,
        'Tank': tank_score,
        'Total': total_score
    })

score_frame = pd.DataFrame(scores)
score_frame = score_frame.sort_values(by='Total', ascending=False)
score_frame['rank'] = list(range(1, voters+1))
print(score_frame)

print(score_frame.head(20))
print(score_frame.tail(20))