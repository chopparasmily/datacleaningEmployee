def generate_insights(eda_result):
    """Generate simple data-driven observations."""
    insights=[]

    overview=eda_result.get("overview",{})

    if overview.get("missing_values",0)>0:
        insights.append(
            f"The dataset contains {overview['missing_values']} missing values."
        )
    else:
        insights.append("The dataset contains no missing values.")

    if overview.get("duplicate_rows",0)>0:
        insights.append(
            f"The dataset contains {overview['duplicate_rows']} duplicate rows."
        )
    else:
        insights.append("No duplicate rows were detected.")

    correlations=eda_result.get("correlation",{}).get(
        "strong_correlations",[]
    )

    for item in correlations:
        insights.append(
            f"{item['column_1']} and {item['column_2']} "
            f"have a correlation of {item['correlation']}."
        )

    outliers=eda_result.get("outliers",{})

    for column,data in outliers.items():
        count=data.get("iqr_count",0)

        if count>0:
            insights.append(
                f"{column} contains {count} potential IQR outliers."
            )

    return insights


def generate_report(eda_result):
    """Generate the final EDA report."""
    return {
        "summary":eda_result.get("overview",{}),
        "column_profile":eda_result.get("column_profile"),
        "column_detection":eda_result.get("column_detection",{}),
        "numeric":eda_result.get("numeric",{}),
        "categorical":eda_result.get("categorical",{}),
        "datetime":eda_result.get("datetime",{}),
        "bivariate":eda_result.get("bivariate",{}),
        "correlation":eda_result.get("correlation",{}),
        "outliers":eda_result.get("outliers",{}),
        "insights":generate_insights(eda_result),
        "raw_result":eda_result
    }