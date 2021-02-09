#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from data import enrollment
from matplotlib.ticker import MaxNLocator

from data.enrollment_info import current_schools


def display_students_vs_classrooms_graph(df):
    students = df[["School", "Students", "Year"]].groupby(["School", "Year"]).sum()
    classrooms = df[["School", "Students", "Year"]].groupby(["School", "Year"]).count().rename({"Students": "Classrooms"}, axis=1)

    return students.join(classrooms)


def plot_students_and_classrooms(**kwargs):
    data = kwargs.pop("data")

    classrooms_limits = kwargs.pop("classroomsLimits")
    students_limits = kwargs.pop("studentsLimits")

    ax1 = plt.gca()
    ax1.set_ylim(students_limits)

    ax2 = ax1.twinx()
    ax2.get_yaxis().set_major_locator(MaxNLocator(integer=True))

    ax2.set_ylim(classrooms_limits)

    ax1.plot(data["Year"], data["Students"], color="b")
    ax2.plot(data["Year"], data["Classrooms"], color="r")


def main():
    df = display_students_vs_classrooms_graph(enrollment)

    classrooms_limits = (df["Classrooms"].min() - .5, df["Classrooms"].max() + .5)
    students_limits = (df["Students"].min() - 10, df["Students"].max() + 10)

    df = df.reset_index()
    df = df[df["School"].isin(current_schools)]
    df["School"].cat.remove_unused_categories(inplace=True)

    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", None):
        print(df)

    g = sns.FacetGrid(df.reset_index(), col="School", col_wrap=4)
    g.map_dataframe(plot_students_and_classrooms, classroomsLimits=classrooms_limits, studentsLimits=students_limits)

    students = mpatches.Patch(color="b", label="Students")
    classrooms = mpatches.Patch(color="r", label="Classrooms")

    plt.legend(handles=[students, classrooms], loc=0)

    plt.show()


if __name__ == "__main__":
    main()
