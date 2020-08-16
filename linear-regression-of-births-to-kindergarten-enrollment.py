#!/usr/bin/env python
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

from data.kindergarten import get_births_five_years_ago_and_kindergartener_enrollments


def main():
    df = get_births_five_years_ago_and_kindergartener_enrollments(1990, 2019).rename({"Births Five Years Ago": "Births"}, axis=1).dropna()
    df["Rolling"] = df["Births"].rolling(window=4, min_periods=4).mean()

    lm = smf.ols(formula="Kindergarteners ~ Rolling", data=df.dropna()).fit()

    print(lm.summary())

    new_x = pd.DataFrame({"Rolling": [df["Rolling"].min(), df["Rolling"].max()]})
    predictions = lm.predict(new_x)

    fig, ax = plt.subplots(figsize=(16, 12), dpi=200)

    df.plot(kind="scatter", x="Rolling", y="Kindergarteners", ax=ax)
    plt.plot(new_x, predictions, c="red", linewidth=2)

    ax.set_xlabel("Rolling 4 Year Mean of Births Five Years Ago")

    plt.savefig("./artifacts/" + Path(__file__).stem + ".png")

    if environ.get("SHOW"):
        plt.show()


if __name__ == "__main__":
    main()
