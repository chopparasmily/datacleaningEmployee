import pandas as pd


def analyze_categorical_column(df,column):
    """Generate frequency statistics for one categorical column."""
    series=df[column].dropna()

    frequency=series.value_counts().reset_index()
    frequency.columns=["value","count"]

    frequency["percentage"]=(
        frequency["count"]/frequency["count"].sum()*100
    ).round(2)

    return {
        "unique_values":int(series.nunique()),
        "top_value":frequency.iloc[0]["value"] if not frequency.empty else None,
        "frequency_table":frequency
    }


def analyze_categorical(df,columns):
    """Analyze all categorical columns."""
    result={}

    for column in columns:
        result[column]=analyze_categorical_column(df,column)

    return result