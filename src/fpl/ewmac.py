import pandas as pd
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt
import json
from fpl.player_data import players, positions

def points_ts(pid):
    #print("ewmac commencing...")

    with open(here("data/element_summary/element_summary_"+str(pid)+".json")) as f:
        data = json.load(f)

    df = pd.json_normalize(data['history'])[
        ['element', 'total_points', 'round']
    ]

    # Join names, teams, positions
    names = players()[['PID', 'first_name', 'second_name']]

    df = pd.merge(
        left = df,
        right = names,
        left_on = "element",
        right_on = "PID"
    ).drop(columns=['PID']).rename(
        columns={'round':'GW'}
    )

    ax = sns.lineplot(data=df, x='GW', y='total_points')
    plot = ax.figure
    plt.close(plot)

    result = {'df':df,
              'plot':plot}
    return(result)

def ewmac_ts(pid, short_alpha, long_alpha):
    df = points_ts(pid)['df']
    df['ewma_'+str(short_alpha)] = df['total_points'].ewm(alpha=short_alpha).mean()
    df['ewma_'+str(long_alpha)] = df['total_points'].ewm(alpha=long_alpha).mean()

    df_tidy = df[['GW', 'total_points', 'ewma_'+str(short_alpha), 'ewma_'+str(long_alpha)]].melt(
            id_vars = 'GW',
            var_name= 'statistic',
            value_name= 'value'
        )

    ax = sns.lineplot(data=df_tidy, x='GW', y='value', hue='statistic')
    plot = ax.figure
    plt.close(plot)


    result = {'df':df,
              'plot':plot}

    return(result)

if __name__ == '__main__':
    print(ewmac_ts(pid=10, short_alpha=0.5, long_alpha=0.25)['df'])
