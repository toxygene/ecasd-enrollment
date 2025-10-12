import numpy as _np
import pandas as _pd
from ecasd_enrollment.data import enrollment as _enrollment

current_schools = [
    "Davey",
    "Flynn",
    "Lakeshore",
    "Locust Lane",
    "Longfellow",
    "Manz",
    "Meadowview",
    "Northwoods",
    "Putnam Heights",
    "Robbins",
    "Roosevelt",
    "Sherman"
]

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


def get_yearly_share_per_grade_by_school(start_year, end_year):
    enrollment_for_years = _enrollment[(_enrollment["Year"].astype("int") >= start_year) & (_enrollment["Year"].astype("int") <= end_year)]

    yearly_district_grade_totals = enrollment_for_years.groupby(["Year", "Grade"]).sum().rename({"Students": "District Students"}, axis=1)
    yearly_per_school_grade_totals = enrollment_for_years.groupby(["Year", "Grade", "School"]).sum().rename({"Students": "School Students"}, axis=1)

    comparison = yearly_district_grade_totals.join(yearly_per_school_grade_totals)
    comparison["Share"] = comparison["School Students"] / comparison["District Students"]

    return comparison[comparison.index.isin(range(start_year, end_year+1), level=0)][["Share"]].dropna()


def get_predicted_yearly_share_per_grade_by_school(start_year, end_year):
    years = _pd.CategoricalIndex(range(start_year-1, end_year+1), name="Year", ordered=True)

    return get_yearly_share_per_grade_by_school(start_year - 3, end_year + 1)[["Share"]].unstack().unstack().rolling(window=3, min_periods=3).mean().reindex(years).shift(periods=1).stack().stack().rename({"Share": "Predicted Share"}, axis=1)


def get_students_per_grade_by_year_and_school(start_year, end_year):
    totals = _enrollment[["Year", "School", "Grade", "Students"]].groupby(["Year", "School", "Grade"]).sum().reset_index()

    return totals[(totals["Year"].astype("int") >= start_year) & (totals["Year"].astype("int") <= end_year)].set_index(["Year", "School", "Grade"]).dropna()


def get_students_per_grade_by_year(start_year, end_year):
    totals = _enrollment[["Year", "Grade", "Students"]].groupby(["Year", "Grade"]).sum().reset_index()

    return totals[(totals["Year"] >= start_year) & (totals["Year"].astype("int") <= end_year)].set_index(["Year", "Grade"])


def get_used_capacity_by_school_and_year(start_year, end_year):
    df = _enrollment[(_enrollment["Year"].astype("int") >= start_year) & (_enrollment["Year"].astype("int") <= end_year) & (_enrollment["School"].isin(current_schools))][["Year", "School", "Students"]].groupby(["Year", "School"]).sum().dropna().reset_index()

    return df.set_index(["Year", "School"])[["Students"]]


def get_classrooms_in_use_by_school_and_year(start_year, end_year):
    df = _enrollment[(_enrollment["Year"].astype("int") >= start_year) & (_enrollment["Year"].astype("int") <= end_year) & (_enrollment["School"].isin(current_schools))][["Year", "School", "Students"]].groupby(["Year", "School"]).count().dropna().reset_index().rename({"Students": "Classrooms"}, axis=1)
    return df.set_index(["Year", "School"])[["Classrooms"]]


def get_capacity_and_classrooms_in_use_by_school_and_year(start_year, end_year):
    used_capacity = get_used_capacity_by_school_and_year(start_year, end_year)
    classrooms_in_use = get_classrooms_in_use_by_school_and_year(start_year, end_year)

    df = classrooms_in_use.join(used_capacity).reset_index()
    df["School"] = df["School"].cat.set_categories(_np.sort(df["School"].unique()))

    return df
