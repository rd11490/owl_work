import pandas as pd
import matplotlib.pyplot as plt
import datetime

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

heroes = pd.read_csv('../player_data/phs-2022.csv')

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

# heroes = heroes[heroes['stage'] != 'Summer Showdown']

SUPPORT = 'Support'
DPS = 'DPS'
TANK = 'Tank'

role = {
    'Lucio': SUPPORT, 'Genji': DPS, 'Tracer': DPS, 'Doomfist': TANK, 'Winston': TANK, 'Reaper': DPS, 'Soldier: 76': DPS,
    'Ana': SUPPORT, 'Zarya': TANK, 'Echo': DPS, 'Widowmaker': DPS, 'Ashe': DPS, 'D.Va': TANK, 'Sigma': TANK,
    'Baptiste': SUPPORT,
    'Zenyatta': SUPPORT, 'Symmetra': DPS, 'Moira': SUPPORT, 'Pharah': DPS, 'Sombra': DPS, 'Brigitte': SUPPORT,
    'Mercy': SUPPORT, 'Mei': DPS,
    'Reinhardt': TANK, 'Roadhog': TANK, 'Hanzo': DPS, 'Cassidy': DPS, 'Sojourn': DPS, 'Junkrat': DPS, 'Bastion': DPS,
    'Wrecking Ball': TANK, 'Torbjorn': DPS, 'Orisa': TANK, 'Junker Queen': TANK,
}

heroes['role'] = heroes.apply(lambda row: role[row['hero_name']], axis=1)

print(heroes)


def get_totals_for_role(group, role):
    role_group = group[group['role'] == role]
    final_blows = role_group[role_group['stat_name'] == 'Final Blows']['amount'].sum()
    elims = role_group[role_group['stat_name'] == 'Eliminations']['amount'].sum()
    damage = role_group[role_group['stat_name'] == 'Hero Damage Done']['amount'].sum()

    return final_blows, elims, damage




def get_group_stats(group):
    total_final_blows = group[group['stat_name'] == 'Final Blows']['amount'].sum()
    total_elims = group[group['stat_name'] == 'Eliminations']['amount'].sum()
    total_damage = group[group['stat_name'] == 'Hero Damage Done']['amount'].sum()

    tank_final_blows, tank_elims, tank_damage = get_totals_for_role(group, TANK)

    dps_final_blows, dps_elims, dps_damage = get_totals_for_role(group, DPS)

    support_final_blows, support_elims, support_damage = get_totals_for_role(group, SUPPORT)

    stats.append({
        'total_final_blows': total_final_blows, 'total_elims': total_elims, 'total_damage': total_damage,
        'tank_final_blows': tank_final_blows, 'tank_elims': tank_elims, 'tank_damage': tank_damage,
        'dps_final_blows': dps_final_blows, 'dps_elims': dps_elims, 'dps_damage': dps_damage,
        'support_final_blows': support_final_blows, 'support_elims': support_elims, 'support_damage': support_damage
    })


heroes = heroes[['esports_match_id', 'map_name', 'team_name', 'role', 'stat_name', 'amount']]

heroes = heroes[heroes['stat_name'].isin(['Hero Damage Done', 'Eliminations', 'Final Blows'])]

stats = []
heroes.groupby(by=['esports_match_id', 'map_name', 'team_name']).apply(get_group_stats).reset_index()
stats_frame = pd.DataFrame(stats)
sums = stats_frame.sum()


def print_role_stats(sums, role):
    modifier = 1
    if role is not 'tank':
        modifier = 2
    fb_pct = round(100 * sums[f'{role}_final_blows'] / sums['total_final_blows'], 2)/modifier
    kill_participation = round(100 * sums[f'{role}_elims'] / sums['total_final_blows'], 2)/modifier
    dmg_pct =  round(100 * sums[f'{role}_damage'] / sums['total_damage'], 2)/modifier

    print(
        f'Final Blow Pct: {fb_pct}\nKill Participation: {kill_participation}\nDamage Percent: {dmg_pct}')
    return fb_pct, kill_participation,dmg_pct


print('Tank')
print_role_stats(sums, 'tank')
print('\n')
print('DPS')
print_role_stats(sums, 'dps')
print('\n')
print('Support')
print_role_stats(sums, 'support')
print('\n')



team_stats_arr = []
for t in Teams.West + Teams.East:
    stats = []
    team_stats = heroes[heroes['team_name'] == t]
    team_stats.groupby(by=['esports_match_id', 'map_name', 'team_name']).apply(get_group_stats).reset_index()
    stats_frame = pd.DataFrame(stats)
    sums = stats_frame.sum()

    print(t)
    print('Tank')
    tank_fb, tank_kp, tank_dmg = print_role_stats(sums, 'tank')
    print('DPS')
    dps_fb, dps_kp, dps_dmg = print_role_stats(sums, 'dps')
    print('Support')
    sp_fb, sp_kp, sp_dmg = print_role_stats(sums, 'support')
    print('')

    team_stats_arr.append({
        'team': t,
        'tank_fb': tank_fb,
        'tank_kp': tank_kp,
        'tank_dmg': tank_dmg,
        'dps_fb': dps_fb,
        'dps_kp': dps_kp,
        'dps_dmg': dps_dmg,
        'sp_fb': sp_fb,
        'sp_kp': sp_kp,
        'sp_dmg': sp_dmg
    })

out_frame = pd.DataFrame(team_stats_arr)
out_frame.to_csv('role_stat_breakdown.csv', index=False)