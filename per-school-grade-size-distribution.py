#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data import enrollment
from matplotlib import ticker


def get_per_school_grade_size_distribution_dataframe(enrollment_dataframe):
    return enrollment_dataframe.groupby(["School", "Year", "Grade"]).sum()


def main():
    sns.set(style="whitegrid")

    df = get_per_school_grade_size_distribution_dataframe(enrollment)

    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", None):
        print(df)

    g = sns.FacetGrid(df.reset_index(), col="School", col_wrap=3)
    g.map(sns.boxplot, "Grade", "Students", palette="Set1")

    t = ticker.MultipleLocator(base=10)

    for ax in g.axes:
        ax.yaxis.set_major_locator(t)

    plt.show()


if __name__ == "__main__":
    main()
