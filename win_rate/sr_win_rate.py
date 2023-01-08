import matplotlib.pyplot as plt
import random

starting_sr = 3900
starting_mmr = 4600

k = 50
win_rate = .6


def calculate_elo(curr_elo, curr_mmr, win_rate):
    r1 = 10 ** (curr_elo / 400)
    r2 = 10 ** (curr_mmr / 400)
    e1 = r1 / (r1 + r2)

    rng = random.random()
    if rng <= win_rate:
        s1 = 1.0
    else:
        s1 = 0.0


    err1 = s1 - e1
    new_elo = curr_elo + k * err1
    return new_elo


for win_rate in [.55, .6]:
    games = [0]
    sr = [starting_sr]
    mmr = [starting_mmr]
    for i in range(1, 200):
        games.append(i)
        curr_elo = sr[-1]
        curr_mmr = mmr[-1]
        match_mmr = min(curr_mmr, 4600)
        new_elo = calculate_elo(curr_elo, match_mmr, win_rate)
        new_mmr = calculate_elo(curr_mmr, match_mmr, win_rate)
        sr.append(new_elo)
        mmr.append(new_mmr)

    if win_rate == .45:
        color = 'green'
    elif win_rate == .5:
        color = 'red'
    elif win_rate == .55:
        color = 'red'
    elif win_rate == .6:
        color = 'blue'

    plt.plot(games, sr, label='SR - {} win rate'.format(win_rate), linestyle='solid', color=color)
    plt.plot(games, mmr, label='MMR - {} win rate'.format(win_rate), linestyle='dashed', color=color)

plt.plot([0, 200], [4650, 4650], label='4650 SR', color='k')
plt.legend()
plt.ylim(3900, 5000)
plt.ylabel('SR')
plt.xlabel('Games Played')
plt.show()
