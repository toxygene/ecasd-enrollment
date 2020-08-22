#!/usr/bin/env python
import glob
from os import mkdir, rmdir, unlink
from os.path import dirname, realpath
from pathlib import Path
from jinja2 import Environment, PackageLoader
from data import enrollment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.formula.api as smf
from datetime import datetime


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


def get_capacity_and_classrooms_in_use_by_school_and_year(start_year, end_year):
    used_capacity = get_used_capacity_by_school_and_year(start_year, end_year)
    classrooms_in_use = get_classrooms_in_use_by_school_and_year(start_year, end_year)

    df = classrooms_in_use.join(used_capacity).reset_index()
    df["School"] = df["School"].cat.set_categories(np.sort(df["School"].unique()))

    return df


def generate():
    df = get_capacity_and_classrooms_in_use_by_school_and_year(1995, 2019)

    package_name = Path(__file__).stem
    working_directory = dirname(realpath(__file__))
    artifact_directory = f"{working_directory}/artifacts"

    try:
        for f in glob.glob(f"{artifact_directory}/*"):
            unlink(f)
        rmdir(artifact_directory)
    except FileNotFoundError:
        pass

    mkdir(artifact_directory)

    template_context = {
        "summaries": {},
        "generated_at": datetime.now()
    }

    # Generate linear regression model
    for school_name, sdf in df.groupby(["School"]):
        lm = smf.ols(formula="Classrooms ~ Students", data=sdf.dropna()).fit()

        template_context["summaries"][school_name] = lm.summary()

    # Generate linear regression model graph
    g = sns.lmplot(x="Classrooms", y="Students", col="School", col_wrap=4, data=df, height=3)
    g.set(xlim=(11.5, 24.5))
    g.set(xticks=range(12, 25, 2))

    plt.savefig(f"{artifact_directory}/graph.png", dpi=100)

    env = Environment(
        loader=PackageLoader(package_name, "templates")
    )

    template = env.get_template("README.md.jinja")

    with open(f"{working_directory}/README.md", "w") as f:
        f.write(template.render(template_context))


if __name__ == "__main__":
    generate()
