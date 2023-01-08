import pandas as pd
import datetime
from sklearn.cluster import KMeans

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

heroes = pd.read_csv('./player_data/phs-2022.csv')

pace_stats = heroes[heroes['hero_name'] == 'All Heroes']
pace_stats = pace_stats[pace_stats['stat_name'].isin(['Deaths', 'Final Blows', 'Time Played'])]

pace_stats = pace_stats[['esports_match_id', 'map_name', 'team_name', 'stat_name', 'amount']].groupby(by=['esports_match_id', 'map_name','team_name', 'stat_name', ]).sum().reset_index()


paces = []
def calculate_pace(group):
    team = group['team_name'].values[0]
    esports_match_id = group['esports_match_id'].values[0]
    map_name = group['map_name'].values[0]

    deaths = group[group['stat_name'] == 'Deaths']['amount'].values[0]
    final_blows = group[group['stat_name'] == 'Final Blows']['amount'].values[0]
    time_played = group[group['stat_name'] == 'Time Played']['amount'].values[0]

    est_fights = (final_blows+deaths)/7.5
    time_played = time_played/5

    pace = 10 * est_fights / (time_played / 60)

    # 10 * cass_sums[stat] / (cass_sums['Time Played'] / 60


    paces.append({
        'team': team,
        'esports_match_id': esports_match_id,
        'map_name': map_name,
        'pace': pace
    })


pace_stats.groupby(by=['esports_match_id', 'map_name', 'team_name']).apply(calculate_pace)
pace_frame = pd.DataFrame(paces)

heroes = heroes[heroes['hero_name'] != 'All Heroes']


def calc_match_date(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S %Z")
    return parsed.date().strftime("%Y/%m/%d")


def determine_stage(date):
    if date < '2022/06/15':
        return 'Kickoff Clash'
    elif '2022/06/15' < date < '2022/08/10':
        return 'Midseason Madness'
    elif '2022/08/10' < date < '2022/09/20':
        return 'Summer Showdown'
    elif '2022/09/20' < date < '2022/10/29':
        return 'Countdown Cup'
    else:
        return 'Playoffs'


heroes['match_date'] = heroes['start_time'].apply(calc_match_date)
heroes['stage'] = heroes['match_date'].apply(determine_stage)

interesting_stats = ['Time Played']

heroes_care = heroes[heroes['stat_name'].isin(interesting_stats)]
hero_sums = heroes_care[['team_name', 'hero_name', 'esports_match_id', 'stage', 'map_name', 'amount']].groupby(
    by=['team_name', 'hero_name', 'stage', 'map_name', 'esports_match_id']).sum().reset_index()


def calculate_play_percent(group):
    group['Percent Played'] = 5 * 100 * group['amount'] / group['amount'].sum()
    return group


hero_sums = hero_sums.groupby(by=['team_name', 'esports_match_id', 'map_name', 'stage']).apply(calculate_play_percent)

hero_sums = hero_sums.pivot(index=['team_name', 'esports_match_id', 'map_name', 'stage'], columns='hero_name',
                            values='Percent Played').fillna(
    0.0).reset_index()
hero_sums['Label'] = hero_sums['team_name'] + '-' + hero_sums['stage'] + '-' + hero_sums['map_name'] + '-' + hero_sums[
    'esports_match_id'].astype(str)
hero_pct_np = hero_sums.to_numpy()
X = hero_pct_np[:, 4:-1]
Y_label = hero_pct_np[:, -1]

clusters = 8
kmeans = KMeans(n_clusters=clusters, random_state=0)
kmeans.fit(X)
labels = kmeans.labels_
df = pd.DataFrame({'Team': Y_label, 'Classification': labels})
print(df)


def split_label(row):
    row['Team Name'] = row['Team'].split('-')[0]
    row['Map Name'] = row['Team'].split('-')[2]
    row['Match Id'] = int(row['Team'].split('-')[3])
    return row


df = df.apply(split_label, axis=1)
df = df[['Team Name', 'Match Id', 'Map Name', 'Classification']]

centers = pd.DataFrame(kmeans.cluster_centers_)
centers.columns = hero_sums.columns[4:-1]
centers = centers.round(2)
centers['Label'] = [i for i in range(0, clusters)]

comps = []

for ind in centers.index:
    row = centers.iloc[ind, :]
    comp = ','.join(row[row > 60].index.tolist())
    comps.append({'Label': comp, "Cluster": row['Label']})

comps_df = pd.DataFrame(comps)
comps_df.to_csv('out/comps_list_2022.csv', index=False)

heroes_with_cluster = heroes.merge(df, left_on=['team_name', 'esports_match_id', 'map_name'],
                                   right_on=['Team Name', 'Match Id', 'Map Name'])
heroes_with_cluster = heroes_with_cluster[
    ['map_type', 'map_name', 'player_name', 'stat_name', 'hero_name', 'amount', 'match_date', 'stage', 'Team Name',
     'Match Id', 'Classification']]
heroes_with_cluster.columns = ['Map Type', 'Map Name', 'Player', 'Stat', 'Hero', 'Amount', 'Match Date', 'Stage',
                               'Team Name', 'Match Id', 'Classification']

opponents = heroes_with_cluster[['Match Id', 'Map Name', 'Team Name', 'Classification']].drop_duplicates()
opponents.columns = ['Match Id', 'Map Name', 'Opponent Team Name', 'Opponent Classification']
heroes_with_cluster = heroes_with_cluster.merge(opponents, on=['Match Id', 'Map Name'])
heroes_with_cluster = heroes_with_cluster[heroes_with_cluster['Team Name'] != heroes_with_cluster['Opponent Team Name']]

stats_to_care = [
    'All Damage Done',
    'Assists',
    'Barrier Damage Done',
    'Damage - Quick Melee',
    'Damage Done',
    'Damage Taken',
    'Deaths',
    'Defensive Assists',
    'Eliminations',
    'Environmental Kills',
    'Final Blows',
    'Healing Done',
    'Hero Damage Done',
    'Knockback Kills',
    'Objective Kills',
    'Objective Time',
    'Offensive Assists',
    'Shots Fired',
    'Time Alive',
    'Time Building Ultimate',
    'Time Holding Ultimate',
    'Time Played',
    'Ultimates Earned - Fractional',
    'Ultimates Used',
    'Amped Heal Activations',
    'Amped Speed Activations',
    'Critical Hit Kills',
    'Critical Hits',
    'Damage - Weapon Primary',
    'Damage - Weapon Secondary',
    'Games Played',
    'Games Won',
    'Heal Song Time Elapsed',
    'Healing - Healing Boost',
    'Healing - Healing Boost Amped',
    'Healing Received',
    'Players Knocked Back',
    'Quick Melee Hits',
    'Quick Melee Ticks',
    'Self Healing',
    'Shots Hit',
    'Shots Missed',
    'Sound Barrier Casts',
    'Sound Barriers Provided',
    'Soundwave Kills',
    'Speed Song Time Elapsed',
    'Melee Final Blows',
    'Damage - Deflect',
    'Damage - Dragonblade',
    'Damage - Dragonblade Total',
    'Damage - Swift Strike',
    'Damage - Swift Strike Dragonblade',
    'Damage Reflected',
    'Deflection Kills',
    'Dragonblade Kills',
    'Dragonblades',
    'Damage - Weapon',
    'Health Recovered',
    'Match Blinks Used',
    'Recalls Used',
    'Damage Blocked',
    'Solo Kills',
    'Ability Damage Done',
    'Damage - Rocket Punch',
    'Damage - Seismic Slam',
    'Shields Created',
    'Damage - Jump Pack',
    'Damage - Primal Rage Leap',
    'Damage - Primal Rage Melee',
    'Damage - Primal Rage Total',
    'Jump Pack Kills',
    'Melee Kills',
    'Primal Rage Kills',
    'Primal Rage Melee Hits',
    'Primal Rage Melee Hits - Multiple',
    'Primal Rage Melee Ticks',
    'Tesla Cannon Hits',
    'Tesla Cannon Hits - Multiple',
    'Tesla Cannon Ticks',
    'Weapon Kills',
    'Damage - Death Blossom',
    'Death Blossom Kills',
    'Death Blossoms',
    'Biotic Field Healing Done',
    'Biotic Fields Deployed',
    'Damage - Helix Rockets',
    'Damage - Tactical Visor',
    'Helix Rocket Kills',
    'Tactical Visor Kills',
    'Tactical Visors',
    'Biotic Grenade Kills',
    'Damage - Biotic Grenade',
    'Damage - Weapon Scoped',
    'Enemies Slept',
    'Healing - Biotic Grenade',
    'Healing - Weapon',
    'Healing - Weapon Scoped',
    'Healing Amplified',
    'Nano Boost Assists',
    'Nano Boosts Applied',
    'Scoped Hits',
    'Scoped Shots',
    'Sleep Dart Hits',
    'Sleep Dart Shots',
    'Unscoped Hits',
    'Unscoped Shots',
    'Environmental Deaths',
    'Damage - Graviton Surge',
    'Energy Maximum',
    'Graviton Surge Kills',
    'High Energy Kills',
    'Lifetime Energy Accumulation',
    'Primary Fire Hits',
    'Primary Fire Ticks',
    'Projected Barriers Applied',
    'Damage - Duplicate',
    'Damage - Focusing Beam',
    'Damage - Focusing Beam - Bonus Damage Only',
    'Damage - Sticky Bombs',
    'Duplicate Kills',
    'Focusing Beam Dealing Damage Seconds',
    'Focusing Beam Kills',
    'Focusing Beam Seconds',
    'Sticky Bombs Direct Hits',
    'Sticky Bombs Kills',
    'Sticky Bombs Used',
    'Damage - Pulse Bomb',
    'Scoped Critical Hit Kills',
    'Scoped Critical Hits',
    'Bob Gun Damage',
    'Bob Kills',
    'Coach Gun Kills',
    'Damage - Bob',
    'Damage - Coach Gun',
    'Damage - Dynamite',
    'Dynamite Kills',
    'Damage - Boosters',
    'Damage - Micro Missiles',
    'Damage - Pistol',
    'Damage - Self Destruct',
    'Mech Deaths',
    'Mechs Called',
    'Self-Destructs',
    'Recon Assists',
    'Damage - Venom Mine',
    'Infra-sight Uptime',
    'Venom Mine Kills',
    'Multikills',
    'Accretion Kills',
    'Accretion Stuns',
    'Damage - Accretion',
    'Damage - Hyperspheres',
    'Damage Absorbed',
    'Gravitic Flux Damage Done',
    'Gravitic Flux Kills',
    'Hyperspheres Direct Hits',
    'Pulse Bomb Kills',
    'Pulse Bombs Attached',
    'Amplification Matrix Assists',
    'Amplification Matrix Casts',
    'Biotic Launcher Healing Explosions',
    'Biotic Launcher Healing Shots',
    'Damage Amplified',
    'Damage Prevented',
    'Healing - Biotic Launcher',
    'Healing - Regenerative Burst',
    'Immortality Field Deaths Prevented',
    'Damage - Discord Orb',
    'Damage - Weapon Charged',
    'Discord Orb Time',
    'Harmony Orb Time',
    'Healing - Harmony Orb',
    'Healing - Transcendence',
    'Transcendence Healing',
    'Time Discorded',
    'Players Teleported',
    'Teleporter Uptime',
    'Teleporters Placed',
    'Biotic Orb Maximum Damage',
    'Biotic Orb Maximum Healing',
    'Coalescence Healing',
    'Damage - Biotic Orb',
    'Damage - Coalescence',
    'Healing - Biotic Orb',
    'Healing - Coalescence',
    'Healing - Secondary Fire',
    'Secondary Fire Hits',
    'Secondary Fire Ticks',
    'Enemies EMP\'d',
    'Enemies Hacked',
    'Time Hacked',
    'Armor - Rally',
    'Armor Provided',
    'Damage - Shield Bash',
    'Healing - Inspire',
    'Healing - Repair Pack',
    'Inspire Uptime',
    'Damage - Meteor Strike',
    'Meteor Strike Kills',
    'Blizzard Kills',
    'Damage - Blizzard',
    'Enemies Frozen',
    'Freeze Spray Damage',
    'Icicle Damage',
    'Successful Freezes',
    'Total Time Frozen',
    'Healing - Immortality Field',
    'Charge Kills',
    'Damage - Charge',
    'Damage - Earthshatter',
    'Damage - Fire Strike',
    'Earthshatter Kills',
    'Earthshatter Stuns',
    'Fire Strike Kills',
    'Rocket Hammer Melee Hits',
    'Rocket Hammer Melee Hits - Multiple',
    'Rocket Hammer Melee Ticks',
    'Damage - Chain Hook',
    'Enemies Hooked',
    'Hooks Attempted',
    'Healing - Weapon Valkyrie',
    'Players Resurrected',
    'Players Saved',
    'Damage - Call Mech',
    'Coalescence Kills',
    'Damage - Bob Charge',
    'Barrage Kills',
    'Damage - Barrage',
    'Rocket Barrages',
    'Rocket Direct Hits',
    'of Rockets Fired',
    'Self-Destruct Kills',
    'Teleporter Pads Destroyed',
    'Damage - Dragonstrike',
    'Damage - Sonic',
    'Damage - Storm Arrows',
    'Dragonstrike Kills',
    'Storm Arrow Kills',
    'Railgun Shots',
    'Damage - Sentry Turret',
    'Photon Projector Kills',
    'Primary Fire Hits Hits - Level',
    'Secondary Direct Hits',
    'Sentry Turret Kills',
    'Turrets Destroyed',
    'Concussion Mine Kills',
    'Damage - Concussion Mine',
    'Damage - RIP-Tire',
    'Damage - Steel Trap',
    'Damage - Total Mayhem',
    'Enemies Trapped',
    'Frag Launcher Direct Hits',
    'Assault Damage',
    'Damage - Weapon Sentry',
    'Sentry Kills',
    'Ultimates Negated',
    'Blaster Kills',
    'Damage - Weapon Pistol',
    'Damage - Weapon Recon',
    'Grenade Damage',
    'Grappling Claw Uses',
    'Roll Uptime',
    'Roll Uses',
    'Damage - Deadeye',
    'Deadeye Kills',
    'Damage - Molten Core',
    'Overload Kills',
    'Torbjörn Kills',
    'Turret Damage',
    'Turret Kills',
    'Damage - Railgun',
    'Railgun Hits',
    'Fan the Hammer Kills',
    'Adaptive Shield Uses',
    'Air Uptime',
    'Damage - Grappling Claw',
    'Damage Taken - Adaptive Shield',
    'Damage Taken - Ball',
    'Grappling Claw Impacts',
    'Shielding - Adaptive Shield',
    'Recon Kills',
    'Molten Core Kills',
    'Damage - Piledriver',
    'Damage Taken - Tank',
    'Grappling Claw Kills',
    'Piledriver Kills',
    'Piledriver Uses',
    'Javelin Damage',
    'Overclock Kills',
    'Railgun Critical Hit Kills',
    'Railgun Critical Hits',
    'Railgun Kills',
    'Damage - Minefield',
    'Minefield Kills',
    'RIP-Tire Kills',
    'Damage - Whole Hog',
    'Whole Hog Kills',
    'Carnage Kills',
    'Jagged Blade Attempts',
    'Jagged Blade Hits',
    'Jagged Blade Kills',
    'Rampage Kills',
    'Wound Uptime',
    'Terra Surge Kills',
]

heroes_with_cluster = heroes_with_cluster[heroes_with_cluster['Stat'].isin(stats_to_care)]

print(heroes_with_cluster)
print(pace_frame)

heroes_with_cluster.to_csv('./out/hero_data_2022.csv', index=False)
heroes_with_cluster[['Team Name', 'Player']].groupby(by='Player').last().reset_index().drop_duplicates().to_csv(
    'out/teams_players_2022.csv', index=False)
heroes_with_cluster[['Stat']].drop_duplicates().to_csv('out/stats_2022.csv', index=False)
heroes_with_cluster[['Stage']].drop_duplicates().to_csv('out/stage_2022.csv', index=False)
heroes_with_cluster[['Hero']].drop_duplicates().to_csv('out/heroes_2022.csv', index=False)
heroes_with_cluster[['Map Type']].drop_duplicates().to_csv('out/map_types_2022.csv', index=False)
heroes_with_cluster[['Map Name']].drop_duplicates().to_csv('out/map_names_2022.csv', index=False)
