import pandas as pd


def analyze_numeric_column(df,column):
    """Calculate descriptive statistics for one numeric column."""
    series=df[column].dropna()

    if series.empty:
        return {}

    return {
        "count":int(series.count()),
        "mean":float(series.mean()),
        "median":float(series.median()),
        "std":float(series.std()),
        "min":float(series.min()),
        "max":float(series.max()),
        "q1":float(series.quantile(0.25)),
        "q3":float(series.quantile(0.75)),
        "skewness":float(series.skew())
    }


def analyze_numeric(df,columns):
    """Analyze all numeric columns."""
    result={}

    for column in columns:
        result[column]=analyze_numeric_column(df,column)

    return result