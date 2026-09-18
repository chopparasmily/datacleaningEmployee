import pandas as pd


def _is_identifier(column):
    """Check whether a column name looks like an identifier."""
    name=column.lower().replace("_"," ").replace("-"," ")
    keywords=["id","code","number","employee id","customer id","account id"]
    return any(keyword in name for keyword in keywords)


def _is_datetime_column(series):
    """Check whether a column contains datetime-like values."""
    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    if series.dtype!="object":
        return False

    converted=pd.to_datetime(series,errors="coerce",format="mixed")
    return converted.notna().mean()>=0.8


def detect_columns(df):
    """Detect useful semantic groups of columns."""
    result={
        "numeric":[],
        "categorical":[],
        "datetime":[],
        "boolean":[],
        "identifier":[],
        "text":[],
        "constant":[],
        "empty":[]
    }

    for column in df.columns:
        series=df[column]

        if series.dropna().empty:
            result["empty"].append(column)
            continue

        if series.nunique(dropna=True)<=1:
            result["constant"].append(column)
            continue

        if _is_identifier(column):
            result["identifier"].append(column)
            continue

        if pd.api.types.is_bool_dtype(series):
            result["boolean"].append(column)
            continue

        if pd.api.types.is_numeric_dtype(series):
            result["numeric"].append(column)
            continue

        if _is_datetime_column(series):
            result["datetime"].append(column)
            continue

        unique_ratio=series.nunique(dropna=True)/max(series.notna().sum(),1)

        if unique_ratio>0.5:
            result["text"].append(column)
        else:
            result["categorical"].append(column)

    return result