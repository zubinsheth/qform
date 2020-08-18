import pandas as pd
import numpy as np


# Func to check for eligibility based on threshold
# Return 1 if greater than condition matches else 0
def score(row, col, threshold):
    if row[col] >= threshold:
        return 1
    else:
        return 0


def rfm(ball_data, PLAYER, favorable_score):
    vk = ball_data.loc[(ball_data["batsman"] == PLAYER)]
    vk = vk[["match_id", "inning", "over", "batsman_runs"]]
    vk = pd.pivot_table(vk, index=["match_id"], values=["batsman_runs"], aggfunc=np.sum)
    vk["match_num"] = np.arange(len(vk))
    vk["match_num"] = len(vk) - vk["match_num"]
    vk["eligible"] = vk.apply(
        lambda row: score(row, "batsman_runs", favorable_score), axis=1
    )
    vk["recency_score"] = vk["eligible"] / vk["match_num"]

    final_recency_score = np.sum(vk["recency_score"] / len(vk["recency_score"]))
    final_frequency_score = np.sum(vk["eligible"] / len(vk["eligible"]))
    final_monetory_score = np.sum(vk["eligible"] * vk["batsman_runs"]) / len(
        vk["eligible"]
    )

    rfm_score = final_recency_score + final_frequency_score + final_monetory_score

    return (
        PLAYER,
        final_recency_score,
        final_frequency_score,
        final_monetory_score,
        rfm_score,
    )

