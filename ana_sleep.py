import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

csvs = os.listdir('player_data') # Get all files in the data directory
frames = []

for file in csvs:
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('player_data', file))
    # Update column names so that they are consistent across years
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    # Add the dataframe to a list
    frames.append(frame)


# Concat all of the dataframes together
player_frame = pd.concat(frames)



# Find out which player is the most successful at getting sleeps on Ana
ana_sleep = player_frame[(player_frame['hero'] == 'Ana') & ((player_frame['stat_name'] == 'Time Played') |  (player_frame['stat_name'] == 'Sleep Dart Shots')|  (player_frame['stat_name'] == 'Sleep Dart Hits'))]



ana_sleep = ana_sleep[['player', 'stat_name','stat_amount']]
def calculate_sleep_dart_rate(group):
    play_time = group[group['stat_name'] == 'Time Played']['stat_amount'].sum()
    sleeps_hit = group[group['stat_name'] == 'Sleep Dart Hits']['stat_amount'].sum()
    sleeps_shot = group[group['stat_name'] == 'Sleep Dart Shots']['stat_amount'].sum()

    return pd.Series({
        'sleep_darts_shot': sleeps_shot,
        'sleep_darts_hit': sleeps_hit,
        'play_time': play_time,
        'sleep_dart_rate': 12*sleeps_shot/play_time,
        'sleep_dart_accuracy': sleeps_hit / sleeps_shot
    })



ana_sleep = ana_sleep.groupby(by='player').apply(calculate_sleep_dart_rate)
ana_sleep = ana_sleep[ana_sleep['sleep_darts_shot'] >= 100]
sleep_stats = ana_sleep.sort_values(by='sleep_dart_rate', ascending=False).reset_index()
print('Sleep Dart Shot Rate (min 100 attempts)')
print(sleep_stats.head(100))

plt.scatter(100 * sleep_stats['sleep_dart_rate'], 100 * sleep_stats['sleep_dart_accuracy'])
plt.xlabel('% of Time on Cooldown')
plt.xlim((20,50))
plt.ylim((20,50))
plt.ylabel('% of Sleep Darts Hit')
plt.show()