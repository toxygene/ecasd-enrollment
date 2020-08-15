import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data import enrollment


def get_capacity_vs_classrooms(enrollment_dataframe):
    school_grade_available_seats = pd.DataFrame([
        ("Davey", "K", 75), ("Davey", "1", 75), ("Davey", "2", 75), ("Davey", "3", 75),
        ("Davey", "4", 87), ("Davey", "5", 87),
        ("Flynn", "K", 50), ("Flynn", "1", 50), ("Flynn", "2", 50), ("Flynn", "3", 50),
        ("Flynn", "4", 58), ("Flynn", "5", 58),
        ("Lakeshore", "K", 75), ("Lakeshore", "1", 75), ("Lakeshore", "2", 75),
        ("Lakeshore", "3", 75), ("Lakeshore", "4", 87), ("Lakeshore", "5", 87),
        ("Locust Lane", "K", 75), ("Locust Lane", "1", 75), ("Locust Lane", "2", 75),
        ("Locust Lane", "3", 75), ("Locust Lane", "4", 87), ("Locust Lane", "5", 87),
        ("Longfellow", "K", 75), ("Longfellow", "1", 75), ("Longfellow", "2", 75),
        ("Longfellow", "3", 75), ("Longfellow", "4", 87), ("Longfellow", "5", 87),
        ("Manz", "K", 75), ("Manz", "1", 75), ("Manz", "2", 75), ("Manz", "3", 75),
        ("Manz", "4", 87), ("Manz", "5", 87),
        ("Meadowview", "K", 75), ("Meadowview", "1", 75), ("Meadowview", "2", 75),
        ("Meadowview", "3", 75), ("Meadowview", "4", 87), ("Meadowview", "5", 87),
        ("Northwoods", "K", 75), ("Northwoods", "1", 75), ("Northwoods", "2", 75),
        ("Northwoods", "3", 75), ("Northwoods", "4", 87), ("Northwoods", "5", 87),
        ("Putnam Heights", "K", 75), ("Putnam Heights", "1", 75), ("Putnam Heights", "2", 75),
        ("Putnam Heights", "3", 75), ("Putnam Heights", "4", 87), ("Putnam Heights", "5", 87),
        ("Robbins", "K", 100), ("Robbins", "1", 100), ("Robbins", "2", 100),
        ("Robbins", "3", 100), ("Robbins", "4", 116), ("Robbins", "5", 116),
        ("Roosevelt", "K", 50), ("Roosevelt", "1", 50), ("Roosevelt", "2", 50),
        ("Roosevelt", "3", 50), ("Roosevelt", "4", 58), ("Roosevelt", "5", 58),
        ("Sherman", "K", 100), ("Sherman", "1", 100), ("Sherman", "2", 100),
        ("Sherman", "3", 100), ("Sherman", "4", 116), ("Sherman", "5", 116)
    ], columns=["School", "Grade", "Maximum Capacity"])

    school_available_seats = school_grade_available_seats[["School", "Maximum Capacity"]].groupby(["School"]).sum()

    year_school_used_seats = enrollment_dataframe.groupby(["Year", "School"]).sum()

    year_school_classrooms = enrollment_dataframe.groupby(["Year", "School"]).count()["Students"]

    school_available_classrooms = pd.DataFrame(
        [("Davey", 18), ("Flynn", 12), ("Lakeshore", 18), ("Locust Lane", 18), ("Longfellow", 18), ("Manz", 18),
         ("Meadowview", 18), ("Northwoods", 18), ("Putnam Heights", 18), ("Robbins", 24), ("Roosevelt", 12),
         ("Sherman", 24)], columns=["School", "Available Classrooms"])

    enrollment_dataframe = year_school_used_seats.reset_index().merge(school_available_seats, on=["School"])
    enrollment_dataframe = enrollment_dataframe.rename(
        {"Students": "Seats in Use", "Maximum Capacity": "Seats Available"}, axis=1)

    enrollment_dataframe["Seat Utilization"] = enrollment_dataframe["Seats in Use"] / enrollment_dataframe[
        "Seats Available"]
    enrollment_dataframe["Capacity Over 85%"] = enrollment_dataframe["Seat Utilization"] > .85

    enrollment_dataframe = enrollment_dataframe.merge(year_school_classrooms, on=["Year", "School"]).rename(
        {"Students": "Classrooms in Use"}, axis=1)
    enrollment_dataframe = enrollment_dataframe.merge(school_available_classrooms)

    enrollment_dataframe["Classroom Utilization"] = enrollment_dataframe["Classrooms in Use"] / enrollment_dataframe[
        "Available Classrooms"]
    enrollment_dataframe["Too Many Classrooms"] = enrollment_dataframe["Classrooms in Use"] > enrollment_dataframe[
        "Available Classrooms"]

    enrollment_dataframe["85% Seat Utilization"] = enrollment_dataframe["Seat Utilization"] + .15

    return enrollment_dataframe


def main():
    df = get_capacity_vs_classrooms(enrollment)

    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", None):
        print(df)

    lower_limit = min(df["85% Seat Utilization"].min(), df["Classroom Utilization"].min()) - .1
    upper_limit = max(df["85% Seat Utilization"].max(), df["Classroom Utilization"].max()) + .1

    fig, axes = plt.subplots(3, 4, sharex="col", sharey="row")

    i = 0
    for school_name, sdf in df.groupby("School"):
        ax = sns.lineplot(x="Year", y="85% Seat Utilization", data=sdf, ax=axes[i // 4][i % 4], color="b")

        ax.axes.set_title(school_name)
        ax.set_ylim(lower_limit, upper_limit)

        sns.lineplot(x="Year", y="Classroom Utilization", data=sdf, ax=ax, color="r")

        i += 1

    fig.legend(["85% Seat Utilization", "Classroom Utilization %"])

    sns.set(style="darkgrid")
    plt.show()


if __name__ == "__main__":
    main()
