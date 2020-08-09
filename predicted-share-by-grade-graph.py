#!/usr/bin/env python

import matplotlib.pyplot as plt
import seaborn as sns

from data.enrollment_info import get_predicted_yearly_share_per_grade_by_school, get_yearly_share_per_grade_by_school


def main():
    yearly_share_per_grade_by_school = get_yearly_share_per_grade_by_school(2012, 2020)
    predicted_yearly_share_per_grade_by_school = get_predicted_yearly_share_per_grade_by_school(2012, 2020)

    df = yearly_share_per_grade_by_school.join(predicted_yearly_share_per_grade_by_school).reset_index().rename({"Share": "Actual", "Predicted Share": "Predicted"}, axis=1)
    df = df.melt(id_vars=["Year", "Grade", "School"], value_vars=["Actual", "Predicted"], var_name="Percent", value_name="Share")

    sns.set_style("darkgrid")
    g = sns.FacetGrid(data=df, row="School", col="Grade")
    g.map(sns.lineplot, "Year", "Share", "Percent")
    g.set(ylim=(0, None))
    g.add_legend()

    plt.savefig("./artifacts/predicted-share-by-grade.png")


if __name__ == "__main__":
    main()
