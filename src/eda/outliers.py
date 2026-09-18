import numpy as np


def calculate_iqr_outliers(series):
    """Calculate the number of IQR-based outliers."""
    values=series.dropna()

    if values.empty:
        return 0

    q1=values.quantile(0.25)
    q3=values.quantile(0.75)
    iqr=q3-q1

    lower=q1-1.5*iqr
    upper=q3+1.5*iqr

    return int(((values<lower)|(values>upper)).sum())


def calculate_zscore_outliers(series,threshold=3):
    """Calculate the number of Z-score based outliers."""
    values=series.dropna()

    if values.empty or values.std()==0:
        return 0

    z_scores=np.abs((values-values.mean())/values.std())

    return int((z_scores>threshold).sum())


def analyze_outliers(df,numeric_columns):
    """Analyze outliers in numeric columns."""
    result={}

    for column in numeric_columns:
        result[column]={
            "iqr_count":calculate_iqr_outliers(df[column]),
            "zscore_count":calculate_zscore_outliers(df[column])
        }

    return result