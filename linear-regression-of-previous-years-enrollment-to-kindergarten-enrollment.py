#!/usr/bin/env python
import statsmodels.formula.api as smf

from data.enrollment_info import get_students_per_grade_by_year


def main():
    df = get_students_per_grade_by_year(2000, 2020).reset_index()
    df = df[df["Grade"] == "K"][["Year", "Students"]]
    df = df.rename({"Students": "This_Years_Students"}, axis=1).merge(df.rename({"Students": "Last_Years_Students"}, axis=1), on="Year")
    df["Last_Years_Students"] = df["Last_Years_Students"].shift(periods=1)

    lm = smf.ols(formula="This_Years_Students ~ Last_Years_Students", data=df.dropna()).fit()
    print(lm.summary())


if __name__ == "__main__":
    main()
