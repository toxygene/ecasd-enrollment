import pandas as _pd

from ecasd_enrollment.data import births as _births
from ecasd_enrollment.data import enrollment as _enrollment
from ecasd_enrollment.data.enrollment_info import get_predicted_yearly_share_per_grade_by_school


def get_births_five_years_ago_and_kindergartener_enrollments(start_year, end_year):
    """
    Create a dataframe where each row contains the enrollments for the year and the number of births five years prior.

    TODO: Fix the years parameter to be (start-5)->end, then filter off the (start-5)->start.

    :param start_year:int
    :param end_year:int
    :return:pd.DataFrame
    """
    years = _pd.CategoricalIndex(range(start_year, end_year+1), name="Year", ordered=True)
    birth_years = _pd.CategoricalIndex(range(start_year-5, end_year+5), name="Year", ordered=True)

    kindergarteners = _enrollment[(_enrollment["Grade"] == "K") & (_enrollment["Year"].astype("int") >= start_year) & (_enrollment["Year"].astype("int") <= end_year)].groupby("Year").sum().rename({"Students": "Kindergarteners"}, axis=1).reindex(years)
    births_five_years_ago = _births.reindex(birth_years).shift(periods=5).rename({"Births": "Births Five Years Ago"}, axis=1)

    df = births_five_years_ago.join(kindergarteners)

    return df[(df.index >= start_year) & (df.index <= end_year)].reindex(years)


def get_ratio_of_births_to_kindergarten_enrollments(start_year, end_year):
    df = get_births_five_years_ago_and_kindergartener_enrollments(start_year, end_year)

    r = (df["Kindergarteners"] / df["Births Five Years Ago"])
    r.name = "Ratio of Kindergarteners to Births Five Years Ago"

    return r


def get_predicted_ratio_of_births_to_kindergarten_enrollments(start_year, end_year):
    years = _pd.CategoricalIndex(range(start_year-3, end_year+1), ordered=True)

    ratios = get_ratio_of_births_to_kindergarten_enrollments(start_year-3, end_year).reindex(years)
    predictions = ratios.rolling(window=3, min_periods=3).mean().shift(periods=1).rename("Predicted Birth To Kindergarten Enrollment Ratio")

    return predictions[(predictions.index >= start_year) * (predictions.index.astype("int") <= end_year)]


def get_predicted_kindergarteners_per_school(start_year, end_year):
    predicted_district_kindergarteners_ratio = get_predicted_ratio_of_births_to_kindergarten_enrollments(start_year, end_year)

    df = _births.shift(periods=5).rename({"Births": "Births Five Years Ago"}, axis=1).join(predicted_district_kindergarteners_ratio)

    predicted_per_grade_share_by_school = get_predicted_yearly_share_per_grade_by_school(start_year, end_year).reset_index()
    predicted_kindergartener_share_by_school = predicted_per_grade_share_by_school[predicted_per_grade_share_by_school["Grade"] == "K"][["Year", "School", "Predicted Share"]].set_index(["Year", "School"])

    df = df.join(predicted_kindergartener_share_by_school)

    prediction = df["Births Five Years Ago"] * df["Predicted Birth To Kindergarten Enrollment Ratio"] * df["Predicted Share"]
    prediction.name = "Predicted"

    return prediction


def get_kindergarten_enrollment_by_year(start_year, end_year):
    yearly_district_kindergarten_enrollment_dataframe = _enrollment.groupby(["Year", "Grade"]).sum().reset_index()
    yearly_district_kindergarten_enrollment_dataframe = yearly_district_kindergarten_enrollment_dataframe[(yearly_district_kindergarten_enrollment_dataframe["Year"].astype("int") >= start_year) & (yearly_district_kindergarten_enrollment_dataframe["Year"].astype("int") <= end_year)]
    yearly_district_kindergarten_enrollment_dataframe = yearly_district_kindergarten_enrollment_dataframe.set_index(["Year"])
    return yearly_district_kindergarten_enrollment_dataframe[yearly_district_kindergarten_enrollment_dataframe["Grade"] == "K"]["Students"].rename("Kindergarteners")
