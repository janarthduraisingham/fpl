import requests, json
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def dataloader():

    base_url = 'https://fantasy.premierleague.com/api/'

    refresh_choice = input("Refresh player data? (y/n) ")

    if refresh_choice not in ["Y", "y"]:
        print("WARNING: Player data will not refresh")

    else:
        print("Refreshing player data...")

        folder_path = Path("data/element_summary")
        folder_path.mkdir(parents=True, exist_ok=True)

        r = requests.get(base_url + 'bootstrap-static/').json()

        with open('data/bootstrap-static.json', 'w') as f:
            json.dump(r, f)

        with open('data/bootstrap-static.json') as f:
            r = json.load(f)

        players = pd.json_normalize(r['elements']).rename(
            columns={'id':'PID'}
        )


        teams = pd.json_normalize(r['teams'])

        positions = pd.json_normalize(r['element_types'])

        df = pd.merge(
            left = players,
            right = teams,
            left_on = 'team',
            right_on = 'id'
        )

        df = df.merge(
            positions,
            left_on = 'element_type',
            right_on = 'id'
    ).rename(
        columns={
            'name':'team_name',
            'singular_name':'position_name'
        }
    )


        # For each gameweek, get all player data: https://fantasy.premierleague.com/api/event/{GID}/
        # For each player, get gameweeek history: https://fantasy.premierleague.com/api/element-summary/{PID}
        pids = df['PID']
        i=0
        for pid in pids:
            i+=1
            print(str(i)+" of "+str(len(df['PID']))+" Loading historical data for "+df[df['PID']==pid]['web_name'].item()+"...")
            pid_gameweek_history = requests.get(base_url + 'element-summary/' + str(pid) + '/').json()

            with open('data/element_summary/element_summary_' + str(pid) + '.json', 'w') as f:
                json.dump(pid_gameweek_history, f)

    refresh_gw_choice = input("Refresh gameweek data? (y/n) ")
    
    if refresh_gw_choice not in ["Y", "y"]:
        print("WARNING: gammeweek data will not refresh")

    else:
        for i in range(38):
            gw=i+1
            print("Loading data for gameweek " + str(gw) + "...")
            gameweek_data = requests.get(base_url + 'event/' + str(gw) + '/live').json()

            with open('data/gw_data/gw_' + str(gw) + '.json', 'w') as f:
                json.dump(gameweek_data, f)


        

if __name__ == '__main__':
    dataloader()

'''
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