import pandas as pd


def prepare_datetime(series):
    """Convert a series to datetime values."""
    return pd.to_datetime(series,errors="coerce",format="mixed")


def analyze_datetime_column(df,column):
    """Analyze year, month and weekday information."""
    series=prepare_datetime(df[column]).dropna()

    if series.empty:
        return {}

    year=series.dt.year.value_counts().sort_index().reset_index()
    year.columns=["year","count"]

    month=series.dt.month.value_counts().sort_index().reset_index()
    month.columns=["month","count"]

    day=series.dt.day_name().value_counts().reset_index()
    day.columns=["day_of_week","count"]

    return {
        "start_date":series.min(),
        "end_date":series.max(),
        "year":year,
        "month":month,
        "day_of_week":day
    }


def analyze_datetime(df,columns):
    """Analyze all datetime columns."""
    result={}

    for column in columns:
        result[column]=analyze_datetime_column(df,column)

    return result