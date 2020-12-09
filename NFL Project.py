
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
games = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\games.csv', index_col = 'gameId')
players =pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\players.csv', index_col = 'nflId')
plays =pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\plays.csv', index_col = ['gameId', 'playId'])
week1 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week1.csv')
week2 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week2.csv')
week3 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week3.csv')
week4 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week4.csv')
week5 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week5.csv')
week6 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week6.csv')
week7 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week7.csv')
week8 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week8.csv')
week9 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week9.csv')
week10 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week10.csv')
week11 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week11.csv')
week12 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week12.csv')
week13 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week13.csv')
week14 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week14.csv')
week15 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week15.csv')
week16 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week16.csv')
week17 = pd.read_csv(r'C:\Users\njfur\Desktop\Kaggle\nfl-big-data-bowl-2021\week17.csv')

def defensive_player(gameid, playid):
    des = plays.loc[(gameid, playid), 'playDescription']
    in_1 = des.find('(', 10)
    in_2 = des.find(')', in_1)
    comma = des.find(',', in_1)
    if in_1 == -1 or in_2 == -1:
        result = 'N/A'
    elif 'sacked' in des:
        result = 'Overturned Strip Sack'
    else:
        if comma == -1 or comma > in_2:
            result = des[in_1+1:in_2]
            if 'thrown' in result:
                return 'N/A'
            elif ';' in result:
                result = []
                result.append(des[in_1+1:des.find(':', in_1)])
                result.append(des[des.find(':', in_1)+1:in_2])
        else:
            result = []
            result.append(des[in_1+1:comma])
            result.append(des[comma+2:in_2])
    return result

def dist(pos1, pos2):
    val = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    return val

def separation(week, gameid, playid, team = 'both'):
    offense = ['QB', 'RB', 'FB', 'WR', 'TE', 'HB']
    defense = ['SS','FS', 'MLB', 'CB', 'LB', 'OLB', 'ILB', 'DL', 'DB', 'NT', 'S', 'DE']
    if team == 'both':
        players = offense + defense
    elif team =='offense':
        players = offense
    elif team == 'defense':
        players = defense
    else:
        return 'Enter {}, {},  or {}'.format('offense', 'defense', 'both')
    dist_to_ball = {}
    football = week[(week['playId']== playid) & (week['gameId'] == gameid) & (week['displayName'] == 'Football')  & ((week['event'] == 'pass_outcome_caught')|(week['event'] == 'pass_outcome_incomplete')| (week['event'] == 'pass_outcome_interception') | (week['event'] == 'pass_outcome_touchdown'))] #| (week['event'] == 'qb_sack')
    if football.empty:
        return 'N/A'
    else:
        ball_pos = football.iloc[0, [1]].item(), football.iloc[0, [2]].item()
        pass_outcome = football.iloc[0, 8]
        if pass_outcome == 'pass_outcome_caught' or pass_outcome == 'pass_outcome_touchdown':
            result = 'C'
        else:
            result = 'I'
    for x in players:
        for index, row in week[(week['playId']== playid) & (week['gameId'] == gameid) & (week['displayName'] != 'Football') & (week['position'] == x) & ((week['event'] == 'pass_outcome_caught')|(week['event'] == 'pass_outcome_incomplete')| (week['event'] == 'pass_outcome_interception') | (week['event'] == 'pass_outcome_touchdown'))].iterrows(): #  | (week['event'] == 'qb_sack')
            player_name = row['displayName']
            player_pos = row['x'], row['y']
            distance = dist(ball_pos, player_pos)
            dist_to_ball[player_name] = distance
    lowest_dist = 100
    lowest_name = ''  
    for key, value in dist_to_ball.items():
        if value < lowest_dist:
            lowest_dist = value
            lowest_name = key
    return lowest_name, lowest_dist, result

def nearest_receiver(week, gameid, playid):
    answer = separation(week, gameid, playid, 'offense')
    return answer
def nearest_defender(week, gameid, playid):
    answer =separation(week, gameid, playid, 'defense')
    return answer

print(nearest_defender(week1, 2018090900, 2037))
week_num = 0
defender_results = {}
for a in [eval('week' + str(x)) for x in range(1, 17)]:
    week_num += 1
    for b in a['gameId'].unique():
        for c in a[a['gameId'] == b]['playId'].unique():
            #print(nearest_defender(a, b, c), week_num, 'game id', b, 'playId', c)
            name = nearest_defender(a, b,c)[0]
            if name != 'N':
                distance = nearest_defender(a, b,c)[1]
                complete = nearest_defender(a, b,c)[2]
                if name in defender_results.keys():
                    defender_results.get(name).append([distance, complete]) 
                else:
                    defender_results[name] = [[distance, complete]]
for key, value in defender_results:
    print(key, value)