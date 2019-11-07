import numpy as np
import pandas as pd
import sqlite3
import statsmodels.api as sm
import statsmodels.formula.api as smf


if __name__ == '__main__':
    data = pd.DataFrame(pd.read_sql_query('SELECT y.name as Year, s.name as School, g.name as Grade, c.students as Students FROM classrooms c JOIN years y ON y.id = c.year_id JOIN schools s ON s.id = c.school_id JOIN grades g ON g.id = c.grade_id', sqlite3.connect("stats.sqlite")))
    results = smf.ols('Students~Year+School+Grade', data=data).fit()
    print(results.summary())