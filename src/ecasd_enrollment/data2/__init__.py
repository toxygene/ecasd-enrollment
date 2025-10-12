from time import strptime

import polars as pl
from importlib.resources import path

schools = [
    "Davey",
    "Flynn",
    "Lakeshore",
    "Locust Lane",
    "Longfellow",
    "Manz",
    "Meadowview",
    "Northwoods",
    "Putnam Heights",
    "Robbins",
    "Roosevelt",
    "Sherman"
]

sections = {
    "Davey": 3,
    "Flynn": 2,
    "Lakeshore": 3,
    "Locust Lane": 3,
    "Longfellow": 3,
    "Manz": 3,
    "Meadowview": 3,
    "Northwoods": 3,
    "Putnam Heights": 3,
    "Robbins": 4,
    "Roosevelt": 2,
    "Sherman": 4
}

def _get_enrollment():
    """Create the enrollment dataframe"""

    df = pl.DataFrame(
        schema={
            "Date": pl.datatypes.Date,
            "School": pl.datatypes.String,
            "Grade": pl.datatypes.String,
            "Students": pl.datatypes.UInt8,
            "School Year": pl.datatypes.String,
            "Cohort Year": pl.datatypes.String,
        }
    )

    with path("ecasd_enrollment", "Third Friday.ods") as f:
        dfs = pl.read_ods(
            source=f,
            sheet_id=0,
            schema_overrides={
                "School": pl.datatypes.String,
                "Grade K": pl.datatypes.UInt8,
                "Grade 1": pl.datatypes.UInt8,
                "Grade 2": pl.datatypes.UInt8,
                "Grade 3": pl.datatypes.UInt8,
                "Grade 4": pl.datatypes.UInt8,
                "Grade 5": pl.datatypes.UInt8,
            }
        )

        for date, ydf in dfs.items():
            year = strptime(date, "%Y-%m-%d").tm_year
            ydf = ydf.with_columns(
                pl.col("School").fill_null(strategy="forward")
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade K"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="K").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year + 5}-{year + 6}").alias("Cohort Year")
                    ).rename({"Grade K": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade 1"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="1").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year + 4}-{year + 5}").alias("Cohort Year")
                    ).rename({"Grade 1": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade 2"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="2").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year + 3}-{year + 4}").alias("Cohort Year")
                    ).rename({"Grade 2": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade 3"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="3").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year + 2}-{year + 3}").alias("Cohort Year")
                    ).rename({"Grade 3": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade 4"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="4").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year + 1}-{year + 2}").alias("Cohort Year")
                    ).rename({"Grade 4": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

            df = pl.concat(
                items=[
                    df,
                    ydf[["School", "Grade 5"]].with_columns(
                        pl.lit(value=date, dtype=pl.datatypes.Date).alias("Date"),
                        pl.lit(value="5").alias("Grade"),
                        pl.lit(value=f"{year}-{year + 1}", dtype=pl.datatypes.String).alias("School Year"),
                        pl.lit(value=f"{year}-{year + 1}").alias("Cohort Year")
                    ).rename({"Grade 5": "Students"}).drop_nulls("Students")
                ],
                how="align"
            )

    return df.sort(by=["School", "School Year"])

enrollment = _get_enrollment()