#!/usr/bin/env python

import matplotlib.pyplot as plt
import seaborn as sns

from data.kindergarten import get_predicted_ratio_of_births_to_kindergarten_enrollments, \
    get_births_five_years_ago_and_kindergartener_enrollments


def main():
    births_and_kindergarteners = get_births_five_years_ago_and_kindergartener_enrollments(2012, 2019)
    predicted_kindergartener_ratio = get_predicted_ratio_of_births_to_kindergarten_enrollments(2012, 2019).rename("Predicted Ratio")

    df = predicted_kindergartener_ratio.to_frame().join(births_and_kindergarteners).rename({"Kindergarteners": "Actual"}, axis=1)
    df["Predicted"] = df["Births Five Years Ago"] * df["Predicted Ratio"]

    df = df.reset_index().melt(id_vars=["Year"], value_vars=["Actual", "Predicted"], var_name="Measurement", value_name="Students")

    sns.set_style("darkgrid")

    g = sns.lineplot(x="Year", y="Students", hue="Measurement", data=df)
    g.set(ylim=(0, None))

    plt.savefig("./artifacts/predicted-number-of-kindergarteners.png")


if __name__ == "__main__":
    main()
