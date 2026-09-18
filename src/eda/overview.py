import pandas as pd


def generate_overview(df):
    """Generate basic dataset information."""
    if df is None:
        raise ValueError("DataFrame cannot be None.")

    numeric_columns=df.select_dtypes(include="number").columns.tolist()
    datetime_columns=df.select_dtypes(include="datetime").columns.tolist()

    categorical_columns=[
        column for column in df.select_dtypes(include="object").columns
        if column not in datetime_columns
    ]

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "total_cells": df.shape[0]*df.shape[1],
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
        "column_names": df.columns.tolist()
    }


def generate_column_profile(df):
    """Generate a profile for every column."""
    profile=[]

    for column in df.columns:
        profile.append({
            "column":column,
            "dtype":str(df[column].dtype),
            "missing":int(df[column].isna().sum()),
            "missing_percentage":round(df[column].isna().mean()*100,2),
            "unique":int(df[column].nunique(dropna=True))
        })

    return pd.DataFrame(profile)