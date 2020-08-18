# standard imports
import pandas as pd
import numpy as np
from rfm import *
import plotly.graph_objects as go
from pathlib import Path

#TEAM = "Royal Challengers Bangalore"
SEASON = 2017
favorable_score = 30

matches_data = pd.read_csv(str(Path.cwd()) + "/data/matches.csv")
# matches_data.head(1)
# matches_data.dtypes
ball_data = pd.read_csv(str(Path.cwd()) + "/data/deliveries.csv")

# Getting all 2017 matches from the dataset for RCB home and away matches
#ids2017 = matches_data.loc[
#    (matches_data["season"] == SEASON)
#    & ((matches_data["team1"] == TEAM) | (matches_data["team2"] == TEAM))
#]
ids2017 = matches_data.loc[(matches_data["season"] == SEASON)]
ids2017 = ids2017["id"].unique()

ball_data = ball_data.loc[(ball_data["match_id"].isin(ids2017))]
#print(ball_data.iloc[1])
#ball_data = ball_data.loc[ ( ball_data['batting_team'] == TEAM)]


rfm_df = pd.DataFrame(
    columns=[
        "batsman",
        "final_recency_score",
        "final_frequency_score",
        "final_monetory_score",
        "rfm_score",
    ]
)

# for each batsman calculate rfm score
for pl in ball_data["batsman"].unique():
    result = rfm(ball_data, pl, favorable_score)
    r = pd.Series(
        {
            "batsman": result[0],
            "final_recency_score": result[1],
            "final_frequency_score": result[2],
            "final_monetory_score": result[3],
            "rfm_score": result[4],
        }
    )
    rfm_df = pd.concat([rfm_df, r.to_frame().T])

rfm_df = rfm_df.sort_values(by=['rfm_score'], ascending=False)
print(rfm_df.head(5))

fig = go.Figure(data=[go.Scatter(
    x=rfm_df['batsman'],
    y=rfm_df['rfm_score'],
    mode='markers')
])

fig.show()