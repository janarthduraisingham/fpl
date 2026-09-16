from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import requests, json
from pyprojroot import here

def players():
    #print("underpriced analysis commencing")

    with open(here('bootstrap-static.json')) as f:
        r = json.load(f)

    players = pd.json_normalize(r['elements']).rename(
        columns={'id':'PID'}
    )
    return(players)

def teams():

    with open(here('bootstrap-static.json')) as f:
            r = json.load(f)

    teams = pd.json_normalize(r['teams'])

    return(teams)

def positions():

    with open(here('bootstrap-static.json')) as f:
            r = json.load(f)

    positions = pd.json_normalize(r['element_types'])

    return(positions)

def player_points(players=players(),
                teams=teams(),
                positions=positions()):
     
     df = pd.merge(
          left = players,
        right = teams,
        left_on = 'team',
        right_on = 'id'
     ).merge(
          positions,
          left_on = 'element_type',
              right_on = 'id'
          ).rename(
              columns={
                  'name':'team_name',
                  'singular_name':'position_name'
              }
          )

     return(df)


def load_element_summary(pid):
    with open(here('data/element_summary/element_summary_'+str(pid)+'.json')) as f:
        r = json.load(f)
    return(r)


def last_2_yrs_points(pid):
    pl = pd.json_normalize(load_element_summary(pid)['history_past'])
    if 'season_name' in pl.columns:
        recent_pl = pl[pl['season_name'].isin(['2024/25', '2025/26'])]
        last_2_year_points = recent_pl['total_points'].sum()
        return(last_2_year_points)
    else:
        return(0)

def last_2_years_points():

     df = player_points()         
     df['points_2yr'] = df['PID'].apply(last_2_yrs_points)
     df['points_per_cost_2yr'] = df['points_2yr'] / df['now_cost']

     return(df[['PID',
'first_name',
'second_name',
'position_name',
'now_cost',
'points_2yr',
'points_per_cost_2yr']])

def last_1_yrs_points(pid):
    pl = pd.json_normalize(load_element_summary(pid)['history_past'])
    if 'season_name' in pl.columns:
        recent_pl = pl[(pl['season_name'] >= '2025/26') & (pl['season_name'] <= '2025/26')]
        last_2_year_points = recent_pl['total_points'].sum()
        return(last_2_year_points)
    else:
        return(0)

def last_1_years_points():

     df = player_points()         
     df['points_2yr'] = df['PID'].apply(last_1_yrs_points)
     df['points_per_cost_2yr'] = df['points_2yr'] / df['now_cost']

     return(df[['PID',
'first_name',
'second_name',
'position_name',
'now_cost',
'points_2yr',
'points_per_cost_2yr']])

#print(last_2_yrs_points(53))

#i = 0
#for pid in pids:
#    i+=1
#    print(str(i) + " pid: " + str(pid) + " " + str(last_2_yrs_points(pid)))


'''
df.sort_values(
    ['position_name', 'points_per_cost_2yr'], ascending=[True, False])[
        ['first_name', 'second_name', 'team_name', 'position_name', 'now_cost', 'total_points', 'points_per_cost',
         'points_2yr',
         'points_per_cost_2yr']
    ].to_csv(
        "output/underpriced.csv")
        
     
df['points_per_cost'] = df['total_points']/df['now_cost']


#df['points_per_cost'].hist(bins=100)
#plt.ylabel('Frequency')
#plt.title('Histogram of col')
#plt.show()

(df[df['points_per_cost']>2]).sort_values(
    ['position_name', 'points_per_cost'], ascending=[True, False])[
        ['first_name', 'second_name', 'team_name', 'position_name', 'now_cost', 'total_points', 'points_per_cost']
    ].to_csv(
        "output/1yr_underpriced.csv")

def load_element_summary(pid):
    with open('data/element_summary/element_summary_'+str(pid)+'.json') as f:
        r = json.load(f)
    return(r)


def last_2_yrs_points(pid):
    pl = pd.json_normalize(load_element_summary(pid)['history_past'])
    if 'season_name' in pl.columns:
        recent_pl = pl[pl['season_name'] >= '2024/25']
        last_2_year_points = recent_pl['total_points'].sum()
        return(last_2_year_points)
    else:
        return(0)

#print(last_2_yrs_points(53))

#i = 0
#for pid in pids:
#    i+=1
#    print(str(i) + " pid: " + str(pid) + " " + str(last_2_yrs_points(pid)))

df['points_2yr'] = df['PID'].apply(last_2_yrs_points)
df['points_per_cost_2yr'] = df['points_2yr'] / df['now_cost']

df.sort_values(
    ['position_name', 'points_per_cost_2yr'], ascending=[True, False])[
        ['first_name', 'second_name', 'team_name', 'position_name', 'now_cost', 'total_points', 'points_per_cost',
         'points_2yr',
         'points_per_cost_2yr']
    ].to_csv(
        "output/underpriced.csv")
        

'''