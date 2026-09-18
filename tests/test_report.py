"""
Tests for the automated EDA report module.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src.visualization.report import (
    generate_eda_report,
    generate_report_sections,
    generate_report_summary,
    get_report_overview,
    get_report_section,
)


def create_test_dataframe():
    """
    Create a representative dataset for report testing.

    Returns
    -------
    pandas.DataFrame
        Sample dataset containing multiple semantic column types.
    """
    return pd.DataFrame(
        {
            "employee_id": [101, 102, 103, 104, 105, 106],
            "age": [22, 25, 30, 35, 40, 45],
            "salary": [
                25000,
                30000,
                40000,
                50000,
                60000,
                70000,
            ],
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
    Recursively close Matplotlib figures contained in a result.

    Parameters
    ----------
    result : object
        Object that may contain Matplotlib figures.
    """
    if isinstance(result, dict):
        for value in result.values():
            close_figures_from_result(value)

    elif isinstance(result, list):
        for item in result:
            close_figures_from_result(item)

    elif hasattr(result, "get_axes"):
        plt.close(result)


def test_generate_report_summary():
    """
    Test generation of the high-level report summary.
    """
    df = create_test_dataframe()

    report = generate_eda_report(df)

    summary = report["summary"]

    assert summary["total_rows"] == 6
    assert summary["total_columns"] == 6
    assert summary["total_cells"] == 36
    assert summary["missing_values"] == 0
    assert summary["duplicate_rows"] == 0

    assert summary["numeric_columns"] >= 2
    assert summary["categorical_columns"] >= 1
    assert summary["datetime_columns"] >= 1
    assert summary["boolean_columns"] >= 1

    close_figures_from_result(report)


def test_generate_report_sections():
    """
    Test report section organization.
    """
    df = create_test_dataframe()

    from src.visualization.eda_engine import run_eda

    eda_result = run_eda(df)

    sections = generate_report_sections(eda_result)

    expected_sections = {
        "dataset_overview",
        "column_profile",
        "column_detection",
        "numeric_analysis",
        "categorical_analysis",
        "datetime_analysis",
        "bivariate_analysis",
        "correlation_analysis",
        "outlier_analysis",
    }

    assert expected_sections.issubset(sections.keys())

    close_figures_from_result(eda_result)


def test_generate_complete_eda_report():
    """
    Test generation of the complete EDA report.
    """
    df = create_test_dataframe()

    report = generate_eda_report(df)

    assert "summary" in report
    assert "sections" in report
    assert "raw_result" in report

    assert isinstance(report["summary"], dict)
    assert isinstance(report["sections"], dict)
    assert isinstance(report["raw_result"], dict)

    close_figures_from_result(report)


def test_get_report_overview():
    """
    Test retrieval of the report overview.
    """
    df = create_test_dataframe()

    report = generate_eda_report(df)

    overview = get_report_overview(report)

    assert isinstance(overview, dict)
    assert overview["total_rows"] == 6
    assert overview["total_columns"] == 6

    close_figures_from_result(report)


def test_get_report_section():
    """
    Test retrieval of an individual report section.
    """
    df = create_test_dataframe()

    report = generate_eda_report(df)

    overview = get_report_section(
        report,
        "dataset_overview",
    )

    assert isinstance(overview, dict)
    assert overview["total_rows"] == 6

    column_profile = get_report_section(
        report,
        "column_profile",
    )

    assert isinstance(column_profile, pd.DataFrame)

    close_figures_from_result(report)


def test_invalid_report_section():
    """
    Test handling of a non-existent report section.
    """
    df = create_test_dataframe()

    report = generate_eda_report(df)

    with pytest.raises(KeyError):
        get_report_section(
            report,
            "invalid_section",
        )

    close_figures_from_result(report)


def test_invalid_report_input():
    """
    Test validation of invalid report input.
    """
    with pytest.raises(TypeError):
        get_report_overview([])


def test_empty_dataframe_report():
    """
    Test that an empty DataFrame cannot generate a report.
    """
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        generate_eda_report(df)


def test_invalid_dataframe_report():
    """
    Test that non-DataFrame input is rejected.
    """
    with pytest.raises(TypeError):
        generate_eda_report([1, 2, 3])