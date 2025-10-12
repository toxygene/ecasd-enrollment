import numpy as _np
import pandas as _pd

from importlib.resources import path as _path
from pyexcel_ods3 import get_data as _get_data


def _calculate_graduation_year(x):
    """Calculate the cohort year for an enrollment record"""
    if x["Grade"] == "K":
        return int(x["Year"]) + 5
    elif x["Grade"] == "1":
        return int(x["Year"]) + 4
    elif x["Grade"] == "2":
        return int(x["Year"]) + 3
    elif x["Grade"] == "3":
        return int(x["Year"]) + 2
    elif x["Grade"] == "4":
        return int(x["Year"]) + 1
    elif x["Grade"] == "5":
        return int(x["Year"])


def _get_enrollment():
    """Create the enrollment dataframe"""
    df = _pd.DataFrame()
    with _path("ecasd_enrollment", "Third Friday.ods") as spreadsheet_path:
        print(_get_data(str(spreadsheet_path)))
        for date, rows in _get_data(str(spreadsheet_path)).items():
            ydf = _pd.DataFrame(rows[1:], columns=rows[0])
            ydf["Date"] = _pd.to_datetime(date)
            ydf = ydf.replace(r"^\s*$", _np.nan, regex=True)
            ydf["School"] = ydf["School"].fillna(method="ffill")
            ydf = _pd.melt(ydf, id_vars=["Date", "School"], var_name="Grade", value_name="Students")
            ydf = ydf[ydf["Students"].notnull()]

            df = _pd.concat([df, ydf])

    df["School"] = _pd.Categorical(df["School"], df["School"].unique())
    df["Students"] = df["Students"].astype("int")
    df["Year"] = _pd.Categorical(df["Date"].apply(lambda x: int(x.strftime("%Y"))), ordered=True)
    df["Grade"] = df["Grade"].transform(lambda x: x[-1:])
    df["Grade"] = _pd.Categorical(df["Grade"], ["K", "1", "2", "3", "4", "5"], ordered=True)
    df["Graduation Year"] = _pd.Categorical(df.apply(_calculate_graduation_year, axis="columns"), ordered=True)

    return df


enrollment = _get_enrollment()

_births = {
    1995: 1011,
    1996: 955,
    1997: 972,
    1998: 919,
    1999: 1005,
    2000: 1004,
    2001: 1053,
    2002: 1039,
    2003: 1009,
    2004: 1020,
    2005: 1074,
    2006: 1070,
    2007: 1035,
    2008: 1073,
    2009: 1017,
    2010: 1001,
    2011: 987,
    2012: 1042,
    2013: 1002,
    2014: 1080,
    2015: 1029,
    2016: 1030,
    2017: 980,
    2018: 945,
    2019: 936
}

births = _pd.DataFrame(data={"Births": list(_births.values())}, index=_pd.CategoricalIndex(list(_births.keys()), name="Year"))
