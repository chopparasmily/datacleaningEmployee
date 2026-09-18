"""
Tests for the automated EDA engine.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src.visualization.eda_engine import (
    generate_column_detection,
    run_eda,
)


def create_test_dataframe():
    """
    Create a representative dataset for EDA engine testing.

    Returns
    -------
    pandas.DataFrame
        Sample dataset containing numeric, categorical,
        boolean, datetime, and identifier columns.
    """
    return pd.DataFrame(
        {
            "employee_id": [101, 102, 103, 104, 105, 106],
            "age": [22, 25, 30, 35, 40, 45],
            "salary": [25000, 30000, 40000, 50000, 60000, 70000],
            "department": [
                "IT",
                "HR",
                "IT",
                "Finance",
                "HR",
                "IT",
            ],
            "joining_date": [
                "2020-01-10",
                "2021-03-15",
                "2021-06-20",
                "2022-01-10",
                "2022-07-12",
                "2023-02-15",
            ],
            "active": [
                True,
                True,
                False,
                True,
                False,
                True,
            ],
        }
    )


def close_figures_from_result(result):
    """
    Close Matplotlib figures stored inside nested EDA results.

    Parameters
    ----------
    result : dict
        EDA result containing Matplotlib figures.
    """
    if isinstance(result, dict):
        for value in result.values():
            close_figures_from_result(value)

    elif isinstance(result, list):
        for item in result:
            close_figures_from_result(item)

    elif hasattr(result, "get_axes"):
        plt.close(result)


def test_generate_column_detection():
    """
    Test automatic column detection integration.
    """
    df = create_test_dataframe()

    result = generate_column_detection(df)

    assert "profile" in result
    assert "groups" in result
    assert "analysis_plan" in result

    assert isinstance(result["profile"], pd.DataFrame)
    assert isinstance(result["groups"], dict)
    assert isinstance(result["analysis_plan"], dict)


def test_run_eda_returns_all_sections():
    """
    Test that the complete EDA engine returns all major sections.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    expected_sections = {
        "overview",
        "column_summary",
        "column_detection",
        "numeric",
        "categorical",
        "datetime",
        "bivariate",
        "correlation",
        "outliers",
    }

    assert expected_sections.issubset(result.keys())

    close_figures_from_result(result)


def test_run_eda_overview():
    """
    Test dataset overview generation through the EDA engine.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    assert result["overview"]["total_rows"] == 6
    assert result["overview"]["total_columns"] == 6

    close_figures_from_result(result)


def test_run_eda_column_summary():
    """
    Test column summary generation through the EDA engine.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    summary = result["column_summary"]

    assert isinstance(summary, pd.DataFrame)
    assert len(summary) == 6
    assert "column" in summary.columns
    assert "detected_type" in summary.columns

    close_figures_from_result(result)


def test_run_eda_numeric_analysis():
    """
    Test automatic numeric visualization generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    assert "age" in result["numeric"]
    assert "salary" in result["numeric"]

    assert result["numeric"]["age"]["histogram"] is not None
    assert result["numeric"]["salary"]["boxplot"] is not None

    close_figures_from_result(result["numeric"])


def test_run_eda_categorical_analysis():
    """
    Test automatic categorical visualization generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    assert "department" in result["categorical"]

    department_result = result["categorical"]["department"]

    assert "frequency_table" in department_result
    assert "count" in department_result
    assert "percentage" in department_result

    assert department_result["frequency_table"] is not None
    assert department_result["count"] is not None
    assert department_result["percentage"] is not None

    close_figures_from_result(result["categorical"])


def test_run_eda_datetime_analysis():
    """
    Test automatic datetime analysis generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    assert "joining_date" in result["datetime"]

    datetime_result = result["datetime"]["joining_date"]

    assert "summary" in datetime_result
    assert "year" in datetime_result
    assert "month" in datetime_result
    assert "day_of_week" in datetime_result
    assert "trend" in datetime_result

    assert datetime_result["summary"] is not None
    assert datetime_result["year"] is not None
    assert datetime_result["month"] is not None
    assert datetime_result["day_of_week"] is not None
    assert datetime_result["trend"] is not None

    close_figures_from_result(result["datetime"])


def test_run_eda_bivariate_analysis():
    """
    Test automatic bivariate analysis generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    assert "numeric_numeric" in result["bivariate"]
    assert "categorical_numeric" in result["bivariate"]

    close_figures_from_result(result["bivariate"])


def test_run_eda_correlation_analysis():
    """
    Test automatic correlation analysis generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    correlation = result["correlation"]

    assert "matrix" in correlation
    assert "strong_correlations" in correlation
    assert "heatmap" in correlation

    assert correlation["matrix"] is not None
    assert correlation["strong_correlations"] is not None

    if correlation["heatmap"] is not None:
        plt.close(correlation["heatmap"])


def test_run_eda_outlier_analysis():
    """
    Test automatic outlier analysis generation.
    """
    df = create_test_dataframe()

    result = run_eda(df)

    outliers = result["outliers"]

    assert "age" in outliers
    assert "salary" in outliers

    assert outliers["age"]["iqr"] is not None
    assert outliers["age"]["zscore"] is not None

    close_figures_from_result(outliers)


def test_empty_dataframe_validation():
    """
    Test that an empty DataFrame is rejected.
    """
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        run_eda(df)


def test_invalid_input_validation():
    """
    Test that non-DataFrame input is rejected.
    """
    with pytest.raises(TypeError):
        run_eda([1, 2, 3])