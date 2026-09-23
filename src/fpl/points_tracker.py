import pandas as pd
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt

def points_tracker(gw):
    points = pd.read_csv(here('data/points_tracker.csv'))
    points = points[points['gw']<=gw].melt(
        id_vars = 'gw',
        var_name= 'team',
        value_name= 'points'
    )

    ax = sns.barplot(data=points, x='gw', y='points', hue = 'team')
    plt.show()


