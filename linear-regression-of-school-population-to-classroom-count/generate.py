#!/usr/bin/env python
from os import getenv, mkdir, remove
from os.path import dirname, realpath
from data import enrollment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.formula.api as smf


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
    df = enrollment[(enrollment["Year"].astype("int") >= start_year) & (enrollment["Year"].astype("int") <= end_year) & (enrollment["School"].isin(sections.keys()))][["Year", "School", "Students"]].groupby(["Year", "School"]).sum().dropna().reset_index()

    return df.set_index(["Year", "School"])[["Students"]]


def get_classrooms_in_use_by_school_and_year(start_year, end_year):
    df = enrollment[(enrollment["Year"].astype("int") >= start_year) & (enrollment["Year"].astype("int") <= end_year) & (enrollment["School"].isin(sections.keys()))][["Year", "School", "Students"]].groupby(["Year", "School"]).count().dropna().reset_index().rename({"Students": "Classrooms"}, axis=1)
    return df.set_index(["Year", "School"])[["Classrooms"]]


def main():
    used_capacity = get_used_capacity_by_school_and_year(1995, 2019)
    classrooms_in_use = get_classrooms_in_use_by_school_and_year(1995, 2019)

    df = classrooms_in_use.join(used_capacity).reset_index()
    df["School"] = df["School"].cat.set_categories(np.sort(df["School"].unique()))

    artifact_directory = f"{dirname(realpath(__file__))}/artifacts"

    try:
        remove(f"{artifact_directory}/*")
    except FileNotFoundError:
        pass

    try:
        mkdir(artifact_directory)
    except FileExistsError:
        pass

    # Generate linear regression model and save results
    for school_name, sdf in df.groupby(["School"]):
        lm = smf.ols(formula="Classrooms ~ Students", data=sdf.dropna()).fit()

        data = f"{school_name}\n{lm.summary()}"

        if getenv("SHOW"):
            print(f"{data}\n\n")

        if getenv("SAVE_ARTIFACTS"):
            with open(f"{artifact_directory}/{school_name}.txt", "w") as f:
                f.write(data)

    # Generate linear regression model graph and save results
    g = sns.lmplot(x="Classrooms", y="Students", col="School", col_wrap=4, data=df, height=3)
    g.set(xlim=(11.5, 24.5))
    g.set(xticks=range(12, 25, 2))

    if getenv("SHOW"):
        plt.show()

    if getenv("SAVE_ARTIFACTS"):
        plt.savefig(f"{artifact_directory}/graph.png", dpi=100)


if __name__ == "__main__":
    main()
