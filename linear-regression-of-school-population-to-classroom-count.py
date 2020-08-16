#!/usr/bin/env python
from os import environ
from pathlib import Path
from data import enrollment
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import pandas as pd


sections = {
    "Davey": 3,
    "Flynn": 2,
    "Lakeshore": 3,
    "Locust Lane": 3,
    "Longfellow": 3,
    "Manz": 3,
    "Meadowview": 3,
    "Northwoods": 3,
    "Putnam Heights": 3,
    "Robbins": 4,
    "Roosevelt": 2,
    "Sherman": 4
}


def get_used_capacity_by_school_and_year(start_year, end_year):
    df = enrollment[(enrollment["Year"] >= start_year) & (enrollment["Year"] <= end_year) & (enrollment["School"].isin(sections.keys()))][["Year", "School", "Students"]].groupby(["Year", "School"]).sum().dropna().reset_index()

    return df.set_index(["Year", "School"])[["Students"]]


def get_classrooms_in_use_by_school_and_year(start_year, end_year):
    df = enrollment[(enrollment["Year"] >= start_year) & (enrollment["Year"] <= end_year) & (enrollment["School"].isin(sections.keys()))][["Year", "School", "Students"]].groupby(["Year", "School"]).count().dropna().reset_index().rename({"Students": "Classrooms"}, axis=1)
    return df.set_index(["Year", "School"])[["Classrooms"]]


def main():
    used_capacity = get_used_capacity_by_school_and_year(2000, 2019)
    classrooms_in_use = get_classrooms_in_use_by_school_and_year(2000, 2019)

    df = classrooms_in_use.join(used_capacity).reset_index()

    fig, axes = plt.subplots(nrows=3, ncols=4, sharex=True, sharey=True, figsize=(16, 12), dpi=200)

    i = 0
    for school_name, sdf in df.groupby(["School"]):
        if school_name not in sections:
            continue

        x = i // 4
        y = i % 4

        g = sdf.plot(kind="scatter", x="Classrooms", y="Students", ax=axes[x][y])
        g.set_title(school_name)

        lm = smf.ols(formula="Classrooms ~ Students", data=sdf.dropna()).fit()

        print(school_name)
        print(lm.summary())
        print()
        print()

        new_y = pd.DataFrame({"Students": [sdf["Students"].min(), sdf["Students"].max()]})
        predictions = lm.predict(new_y)
        predictions.name = "Students"

        g.plot(predictions, new_y, c="red", linewidth=2)

        i += 1

    plt.savefig("./artifacts/" + Path(__file__).stem + ".png")

    if environ.get("SHOW"):
        plt.show()


if __name__ == "__main__":
    main()
