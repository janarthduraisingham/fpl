import pandas as pd
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt
import json

def points_ts(pid):
    print("ewmac commencing...")

    with open(here("data/element_summary/element_summary_"+str(pid)+".json")) as f:
        data = json.load(f)

    df = pd.json_normalize(data['history'])[
        ['element', 'total_points', 'round']
    ]

    #ax = sns.barplot(data=points, x='gw', y='points', hue = 'team')
    #plt.show()
    #print(df.head())
    return(df)

if __name__ == '__main__':
    print(points_ts(10))
    print("complete")