from src.eda.overview import generate_overview,generate_column_profile
from src.eda.column_detector import detect_columns
from src.eda.univariate import analyze_numeric
from src.eda.categorical import analyze_categorical
from src.eda.datetime_analysis import analyze_datetime
from src.eda.bivariate import analyze_bivariate
from src.eda.correlation import analyze_correlation
from src.eda.outliers import analyze_outliers


def generate_eda(df):
    """Run the complete EDA analysis on a DataFrame."""
    if df is None:
        raise ValueError("DataFrame cannot be None.")

    columns=detect_columns(df)

    numeric_columns=columns["numeric"]
    categorical_columns=columns["categorical"]
    datetime_columns=columns["datetime"]

    return {
        "overview":generate_overview(df),
        "column_profile":generate_column_profile(df),
        "column_detection":columns,
        "numeric":analyze_numeric(df,numeric_columns),
        "categorical":analyze_categorical(df,categorical_columns),
        "datetime":analyze_datetime(df,datetime_columns),
        "bivariate":analyze_bivariate(
            df,numeric_columns,categorical_columns
        ),
        "correlation":analyze_correlation(
            df,numeric_columns
        ),
        "outliers":analyze_outliers(
            df,numeric_columns
        )
    }