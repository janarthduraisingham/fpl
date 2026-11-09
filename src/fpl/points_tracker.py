import pandas as pd
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt
from fpl.player_data import initial_squad_tracker

def points_tracker(gw):
    points = pd.read_csv(here('data/points_tracker.csv')).merge(
        initial_squad_tracker()[['GW', 'total_points']],
        left_on = "gw",
        right_on = "GW"
    ).rename(
        columns = {'total_points':'initial 15'}
    )

    points = points[points['gw']<=gw].melt(
        id_vars = ['gw', 'GW'],
        var_name= 'team',
        value_name= 'points'
    )

    sizes = {"me": 3,
             "average": 1,
             "initial 15":1}

    ax = sns.lineplot(data=points, x='gw', y='points', hue = 'team', size='team',
                      sizes = sizes)
    ax.set_ylim(0, 100)
    plt.show()
    

if __name__ == '__main__':
    print(points_tracker(10))
