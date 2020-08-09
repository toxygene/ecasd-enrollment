#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data import enrollment
from matplotlib import ticker


def print_cohort_size_distribution(enrollment_dataframe):
    return enrollment_dataframe.groupby(["School", "Graduation Year", "Grade"]).sum()


def main():
    df = print_cohort_size_distribution(enrollment)

    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", None):
        print(df.dropna())

    sns.set(style="darkgrid")

    g = sns.FacetGrid(df.reset_index().dropna(), col="School", col_wrap=3)
    g.map(sns.scatterplot, "Graduation Year", "Students", "Grade")

    t = ticker.MultipleLocator(base=10)

    for ax in g.axes:
        ax.yaxis.set_major_locator(t)

    plt.savefig("./artifacts/per-school-cohort-size-distribution.png")
    plt.show()


if __name__ == "__main__":
    main()
