import matplotlib.pyplot as plt
import seaborn as sns

from data.enrollment_info import get_students_per_grade_by_year_and_school
from data.kindergarten import get_predicted_kindergarteners_per_school


def main():
    start_year = 1990
    end_year = 2020

    prediction = get_predicted_kindergarteners_per_school(start_year, end_year)

    temp = get_students_per_grade_by_year_and_school(start_year, end_year).reset_index()
    temp = temp[temp["Grade"] == "K"]
    actual = temp.set_index(["Year", "School"])[["Students"]].rename({"Students": "Actual"}, axis=1)

    df = actual.join(prediction).reset_index().melt(id_vars=["Year", "School"], value_vars=["Actual", "Predicted"], var_name="Measurement", value_name="Students")

    sns.set_style("darkgrid")

    g = sns.FacetGrid(df.dropna(), col="School", col_wrap=4)
    g.map(sns.lineplot, "Year", "Students", "Measurement")

    g.add_legend()
    g.set(ylim=0)

    plt.show()


if __name__ == "__main__":
    main()
