import pandas as pd


def analyze_correlation(df,numeric_columns,method="pearson",threshold=0.7):
    """Calculate correlation matrix and strong relationships."""
    if len(numeric_columns)<2:
        return {
            "method":method,
            "threshold":threshold,
            "matrix":pd.DataFrame(),
            "strong_correlations":[]
        }

    matrix=df[numeric_columns].corr(method=method)

    strong=[]

    for i,column1 in enumerate(matrix.columns):
        for column2 in matrix.columns[i+1:]:
            value=matrix.loc[column1,column2]

            if pd.notna(value) and abs(value)>=threshold:
                strong.append({
                    "column_1":column1,
                    "column_2":column2,
                    "correlation":round(float(value),3)
                })

    return {
        "method":method,
        "threshold":threshold,
        "matrix":matrix,
        "strong_correlations":strong
    }