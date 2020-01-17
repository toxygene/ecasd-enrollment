import numpy as np
import pandas as pd
import sqlite3
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from pprint import pprint


if __name__ == '__main__':
    df = pd.DataFrame(pd.read_sql_query('SELECT y.name as Year, s.name as School, s.capacity as Capacity, g.name as Grade, c.students as Students FROM classrooms c JOIN years y ON y.id = c.year_id JOIN schools s ON s.id = c.school_id JOIN grades g ON g.id = c.grade_id', sqlite3.connect("stats.sqlite")))

    # TODO Grade K/1 are missing/combined?
    results = smf.ols('Students ~ Year + School + Grade', data=df).fit()
    print(results.summary())
