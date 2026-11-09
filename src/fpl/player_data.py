from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import requests, json
from pyprojroot import here

def players():
    #print("underpriced analysis commencing")

    with open(here('data/bootstrap-static.json')) as f:
        r = json.load(f)

    players = pd.json_normalize(r['elements']).rename(
        columns={'id':'PID'}
    )
    return(players)

def teams():

    with open(here('data/bootstrap-static.json')) as f:
            r = json.load(f)

    teams = pd.json_normalize(r['teams'])

    return(teams)

def positions():

    with open(here('data/bootstrap-static.json')) as f:
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
        recent_pl = pl[pl['season_name'].isin(['2025/26'])]
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


def points(pid):
      with open(here("data/element_summary/element_summary_"+str(pid)+".json")) as f:
                      data = json.load(f)

                      df = pd.json_normalize(data['history'])[
                           ['element', 'total_points', 'round']
                            ].rename(
                                columns={'round':'GW'}
                            )

      return(df)

def initial_squad_tracker():

     df = players()

     initial_squad = ['Verbruggen', 'Leno',
                      'Mitchell', 'Guéhi', 'Van Hecke', 'Tarkowski', 'N.Williams',
                      'Szoboszlai', 'Rice', 'Anderson', 'Iwobi', 'Damsgaard',
                      'Calvert-Lewin', 'Mateta', 'Welbeck'
                      ]

     initial_squad_pids = ['109', '250',
                           '204', '388', '112', '229', '469',
                           '368', '13', '481', '261', '96',
                           '346', '223', '136'
                           ]

     df = {pid:points(pid) for pid in initial_squad_pids}
     df = pd.concat(df.values(), ignore_index=True).merge(
          players()[['PID', 'second_name']],
          left_on = 'element',
          right_on = 'PID'
     )

     tracker = df.groupby("GW", as_index=False)['total_points'].sum()

     # pro-rate
     tracker['pro_rata_points'] = tracker['total_points']*(12/15)

     return(tracker)


if __name__ == '__main__':
     print("running...")
     print(initial_squad_tracker())
     print("complete")