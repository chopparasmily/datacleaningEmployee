import pandas as pd


def analyze_numeric_relationship(df,x_column,y_column):
    """Analyze the relationship between two numeric columns."""
    data=df[[x_column,y_column]].dropna()

    if data.empty:
        return {}

    correlation=data[x_column].corr(data[y_column])

    return {
        "x_column":x_column,
        "y_column":y_column,
        "correlation":float(correlation),
        "rows_used":len(data)
    }


def analyze_categorical_numeric(df,categorical_column,numeric_column):
    """Analyze a numeric column across categorical groups."""
    data=df[[categorical_column,numeric_column]].dropna()

    if data.empty:
        return {}

    group_stats=data.groupby(categorical_column)[numeric_column].agg(
        ["count","mean","median","min","max"]
    ).reset_index()

    return {
        "categorical_column":categorical_column,
        "numeric_column":numeric_column,
        "group_statistics":group_stats
    }


def analyze_bivariate(df,numeric_columns,categorical_columns):
    """Generate basic bivariate analysis."""
    result={
        "numeric_numeric":{},
        "categorical_numeric":{}
    }

    if len(numeric_columns)>=2:
        x_column=numeric_columns[0]
        y_column=numeric_columns[1]

        result["numeric_numeric"][
            f"{x_column} vs {y_column}"
        ]=analyze_numeric_relationship(
            df,x_column,y_column
        )

    if categorical_columns and numeric_columns:
        categorical_column=categorical_columns[0]
        numeric_column=numeric_columns[0]

        result["categorical_numeric"][
            f"{categorical_column} vs {numeric_column}"
        ]=analyze_categorical_numeric(
            df,categorical_column,numeric_column
        )

    return result