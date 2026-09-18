"""
Tests for the automated visualization column detector.
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.visualization.column_detector import (
    create_analysis_plan,
    get_column_groups,
    profile_columns,
)


def test_column_detection():
    """
    Verify that common column types are detected correctly.
    """

    df = pd.DataFrame(
        {
            "employee_id": [1001, 1002, 1003, 1004],
            "age": [25, 30, 35, 40],
            "salary": [30000, 45000, 60000, 75000],
            "department": ["IT", "HR", "IT", "Finance"],
            "joining_date": [
                "2023-01-01",
                "2023-02-01",
                "2023-03-01",
                "2023-04-01",
            ],
            "is_active": [True, True, False, True],
        }
    )

    groups = get_column_groups(df)

    assert "employee_id" in groups["identifier"]
    assert "age" in groups["numeric"]
    assert "salary" in groups["numeric"]
    assert "department" in groups["categorical"]
    assert "joining_date" in groups["datetime"]
    assert "is_active" in groups["boolean"]


def test_column_profile():
    """
    Verify that column profiling returns expected information.
    """

    df = pd.DataFrame(
        {
            "age": [20, 25, 30, None],
            "department": ["IT", "HR", "IT", "Finance"],
        }
    )

    profile = profile_columns(df)

    assert len(profile) == 2

    assert "column" in profile.columns
    assert "detected_type" in profile.columns
    assert "missing_count" in profile.columns


def test_analysis_plan():
    """
    Verify that the automatic analysis plan is generated.
    """

    df = pd.DataFrame(
        {
            "age": [20, 25, 30, 35],
            "salary": [30000, 40000, 50000, 60000],
            "department": ["IT", "HR", "IT", "Finance"],
        }
    )

    plan = create_analysis_plan(df)

    assert "numeric" in plan
    assert "categorical" in plan
    assert "relationships" in plan

    assert "age" in plan["numeric"]["columns"]
    assert "salary" in plan["numeric"]["columns"]
    assert "department" in plan["categorical"]["columns"]

    assert plan["relationships"]["correlation"] is True


from src.visualization.overview import (
    generate_column_summary,
    generate_overview,
)


def test_generate_overview():
    """
    Verify that dataset-level overview statistics are generated.
    """

    df = pd.DataFrame(
        {
            "age": [20, 25, 30, None],
            "salary": [30000, 40000, 50000, 60000],
            "department": ["IT", "HR", "IT", "Finance"],
        }
    )

    overview = generate_overview(df)

    assert overview["total_rows"] == 4
    assert overview["total_columns"] == 3
    assert overview["missing_values"] == 1
    assert overview["numeric_columns"] == 2
    assert overview["categorical_columns"] == 1


def test_generate_column_summary():
    """
    Verify that column-level summary information is generated.
    """

    df = pd.DataFrame(
        {
            "age": [20, 25, 30],
            "department": ["IT", "HR", "IT"],
        }
    )

    summary = generate_column_summary(df)

    assert len(summary) == 2

    assert "column" in summary.columns
    assert "detected_type" in summary.columns
    assert "missing_percentage" in summary.columns

    age_row = summary[
        summary["column"] == "age"
    ].iloc[0]

    assert age_row["detected_type"] == "numeric"



from src.visualization.univariate import (
    generate_numeric_plots,
    plot_boxplot,
    plot_histogram,
    plot_kde,
)


def test_plot_histogram():
    """
    Verify that a histogram figure is generated.
    """

    df = pd.DataFrame(
        {
            "salary": [
                30000,
                35000,
                40000,
                45000,
                50000,
            ]
        }
    )

    fig = plot_histogram(
        df,
        "salary"
    )

    assert fig is not None

    assert len(fig.axes) == 1


def test_plot_kde():
    """
    Verify that a KDE figure is generated.
    """

    df = pd.DataFrame(
        {
            "salary": [
                30000,
                35000,
                40000,
                45000,
                50000,
                55000,
            ]
        }
    )

    fig = plot_kde(
        df,
        "salary"
    )

    assert fig is not None

    assert len(fig.axes) == 1


def test_plot_boxplot():
    """
    Verify that a boxplot figure is generated.
    """

    df = pd.DataFrame(
        {
            "salary": [
                30000,
                35000,
                40000,
                45000,
                50000,
            ]
        }
    )

    fig = plot_boxplot(
        df,
        "salary"
    )

    assert fig is not None

    assert len(fig.axes) == 1


def test_generate_numeric_plots():
    """
    Verify automatic numeric plot generation.
    """

    df = pd.DataFrame(
        {
            "age": [
                20,
                25,
                30,
                35,
                40,
            ],
            "salary": [
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
            ],
        }
    )

    plots = generate_numeric_plots(df)

    assert "age" in plots

    assert "salary" in plots

    assert "department" not in plots

    assert plots["age"]["histogram"] is not None

    assert plots["age"]["boxplot"] is not None

    assert plots["salary"]["histogram"] is not None



"""
Automated categorical visualization module.

This module creates frequency tables, count distributions,
and percentage distributions for categorical and boolean
columns without requiring hard-coded column names.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.visualization.column_detector import get_column_groups


def _validate_dataframe(df):
    """
    Validate that the supplied object is a pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to validate.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If the supplied object is not a DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame."
        )


def _validate_column(df, column):
    """
    Validate that a requested column exists in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the column.

    column : str
        Column name to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the column does not exist.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the DataFrame."
        )


def _prepare_categories(df, column):
    """
    Prepare categorical values for visualization.

    Missing values are converted to the label 'Missing'.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to prepare.

    Returns
    -------
    pandas.Series
        Clean categorical series.
    """

    values = df[column].copy()

    values = values.astype("object")

    values = values.where(
        values.notna(),
        "Missing"
    )

    return values


def get_frequency_table(df, column, top_n=None):
    """
    Generate a frequency and percentage table for a categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to analyze.

    top_n : int or None, default=None
        Maximum number of categories to return.
        If None, all categories are returned.

    Returns
    -------
    pandas.DataFrame
        Frequency table containing category, count, and percentage.

    Raises
    ------
    TypeError
        If df is not a DataFrame.

    ValueError
        If the column does not exist or contains no usable values.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    values = _prepare_categories(
        df,
        column
    )

    if values.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    counts = (
        values
        .value_counts(dropna=False)
        .reset_index()
    )

    counts.columns = [
        "category",
        "count"
    ]

    total = counts["count"].sum()

    counts["percentage"] = (
        counts["count"] / total * 100
    )

    if top_n is not None:

        if not isinstance(top_n, int):
            raise TypeError(
                "top_n must be an integer or None."
            )

        if top_n <= 0:
            raise ValueError(
                "top_n must be greater than zero."
            )

        counts = counts.head(top_n)

    return counts


def plot_count_distribution(
    df,
    column,
    top_n=15,
    figsize=(10, 6)
):
    """
    Create a count distribution plot for a categorical column.

    Only the top categories are displayed to keep the visualization
    readable for datasets containing many categories.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to visualize.

    top_n : int, default=15
        Number of categories to display.

    figsize : tuple, default=(10, 6)
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
        Generated count distribution figure.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    frequency_table = get_frequency_table(
        df,
        column,
        top_n=top_n
    )

    if frequency_table.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    plot_data = frequency_table.copy()

    plot_data["category"] = (
        plot_data["category"]
        .astype(str)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.barplot(
        data=plot_data,
        x="count",
        y="category",
        ax=ax
    )

    ax.set_title(
        f"{column} - Category Distribution"
    )

    ax.set_xlabel(
        "Count"
    )

    ax.set_ylabel(
        column
    )

    fig.tight_layout()

    return fig


def plot_percentage_distribution(
    df,
    column,
    top_n=15,
    figsize=(10, 6)
):
    """
    Create a percentage distribution plot for a categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to visualize.

    top_n : int, default=15
        Number of categories to display.

    figsize : tuple, default=(10, 6)
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
        Generated percentage distribution figure.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    frequency_table = get_frequency_table(
        df,
        column,
        top_n=top_n
    )

    if frequency_table.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    plot_data = frequency_table.copy()

    plot_data["category"] = (
        plot_data["category"]
        .astype(str)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.barplot(
        data=plot_data,
        x="percentage",
        y="category",
        ax=ax
    )

    ax.set_title(
        f"{column} - Percentage Distribution"
    )

    ax.set_xlabel(
        "Percentage (%)"
    )

    ax.set_ylabel(
        column
    )

    fig.tight_layout()

    return fig


def _is_high_cardinality(
    df,
    column,
    max_categories=30
):
    """
    Determine whether a categorical column has excessive cardinality.

    High-cardinality columns are generally unsuitable for standard
    categorical visualizations because they can produce unreadable
    charts.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the column.

    column : str
        Column to evaluate.

    max_categories : int, default=30
        Maximum number of unique categories considered manageable.

    Returns
    -------
    bool
        True when the column exceeds the configured category limit.
    """

    unique_count = (
        df[column]
        .nunique(dropna=False)
    )

    return unique_count > max_categories


def generate_categorical_plots(
    df,
    top_n=15,
    max_categories=30
):
    """
    Automatically generate categorical visualizations.

    Categorical and boolean columns are detected automatically
    using the column detection engine.

    High-cardinality columns are skipped to prevent unreadable
    visualizations.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to visualize.

    top_n : int, default=15
        Number of top categories displayed in each chart.

    max_categories : int, default=30
        Maximum number of unique categories allowed for plotting.

    Returns
    -------
    dict
        Dictionary containing frequency tables and Matplotlib figures.
    """

    _validate_dataframe(df)

    groups = get_column_groups(df)

    categorical_columns = groups["categorical"]

    boolean_columns = groups["boolean"]

    columns = (
        categorical_columns
        + boolean_columns
    )

    plots = {}

    for column in columns:

        if _is_high_cardinality(
            df,
            column,
            max_categories=max_categories
        ):
            continue

        column_plots = {}

        try:
            column_plots["frequency_table"] = (
                get_frequency_table(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["frequency_table"] = None

        try:
            column_plots["count"] = (
                plot_count_distribution(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["count"] = None

        try:
            column_plots["percentage"] = (
                plot_percentage_distribution(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["percentage"] = None

        plots[column] = column_plots

    return plots
"""
Automated categorical visualization module.

This module creates frequency tables, count distributions,
and percentage distributions for categorical and boolean
columns without requiring hard-coded column names.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.visualization.column_detector import get_column_groups


def _validate_dataframe(df):
    """
    Validate that the supplied object is a pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to validate.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If the supplied object is not a DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame."
        )


def _validate_column(df, column):
    """
    Validate that a requested column exists in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the column.

    column : str
        Column name to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the column does not exist.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the DataFrame."
        )


def _prepare_categories(df, column):
    """
    Prepare categorical values for visualization.

    Missing values are converted to the label 'Missing'.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to prepare.

    Returns
    -------
    pandas.Series
        Clean categorical series.
    """

    values = df[column].copy()

    values = values.astype("object")

    values = values.where(
        values.notna(),
        "Missing"
    )

    return values


def get_frequency_table(df, column, top_n=None):
    """
    Generate a frequency and percentage table for a categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to analyze.

    top_n : int or None, default=None
        Maximum number of categories to return.
        If None, all categories are returned.

    Returns
    -------
    pandas.DataFrame
        Frequency table containing category, count, and percentage.

    Raises
    ------
    TypeError
        If df is not a DataFrame.

    ValueError
        If the column does not exist or contains no usable values.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    values = _prepare_categories(
        df,
        column
    )

    if values.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    counts = (
        values
        .value_counts(dropna=False)
        .reset_index()
    )

    counts.columns = [
        "category",
        "count"
    ]

    total = counts["count"].sum()

    counts["percentage"] = (
        counts["count"] / total * 100
    )

    if top_n is not None:

        if not isinstance(top_n, int):
            raise TypeError(
                "top_n must be an integer or None."
            )

        if top_n <= 0:
            raise ValueError(
                "top_n must be greater than zero."
            )

        counts = counts.head(top_n)

    return counts


def plot_count_distribution(
    df,
    column,
    top_n=15,
    figsize=(10, 6)
):
    """
    Create a count distribution plot for a categorical column.

    Only the top categories are displayed to keep the visualization
    readable for datasets containing many categories.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to visualize.

    top_n : int, default=15
        Number of categories to display.

    figsize : tuple, default=(10, 6)
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
        Generated count distribution figure.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    frequency_table = get_frequency_table(
        df,
        column,
        top_n=top_n
    )

    if frequency_table.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    plot_data = frequency_table.copy()

    plot_data["category"] = (
        plot_data["category"]
        .astype(str)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.barplot(
        data=plot_data,
        x="count",
        y="category",
        ax=ax
    )

    ax.set_title(
        f"{column} - Category Distribution"
    )

    ax.set_xlabel(
        "Count"
    )

    ax.set_ylabel(
        column
    )

    fig.tight_layout()

    return fig


def plot_percentage_distribution(
    df,
    column,
    top_n=15,
    figsize=(10, 6)
):
    """
    Create a percentage distribution plot for a categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the categorical column.

    column : str
        Categorical column to visualize.

    top_n : int, default=15
        Number of categories to display.

    figsize : tuple, default=(10, 6)
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
        Generated percentage distribution figure.
    """

    _validate_dataframe(df)

    _validate_column(df, column)

    frequency_table = get_frequency_table(
        df,
        column,
        top_n=top_n
    )

    if frequency_table.empty:
        raise ValueError(
            f"Column '{column}' does not contain usable values."
        )

    plot_data = frequency_table.copy()

    plot_data["category"] = (
        plot_data["category"]
        .astype(str)
    )

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.barplot(
        data=plot_data,
        x="percentage",
        y="category",
        ax=ax
    )

    ax.set_title(
        f"{column} - Percentage Distribution"
    )

    ax.set_xlabel(
        "Percentage (%)"
    )

    ax.set_ylabel(
        column
    )

    fig.tight_layout()

    return fig


def _is_high_cardinality(
    df,
    column,
    max_categories=30
):
    """
    Determine whether a categorical column has excessive cardinality.

    High-cardinality columns are generally unsuitable for standard
    categorical visualizations because they can produce unreadable
    charts.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the column.

    column : str
        Column to evaluate.

    max_categories : int, default=30
        Maximum number of unique categories considered manageable.

    Returns
    -------
    bool
        True when the column exceeds the configured category limit.
    """

    unique_count = (
        df[column]
        .nunique(dropna=False)
    )

    return unique_count > max_categories


def generate_categorical_plots(
    df,
    top_n=15,
    max_categories=30
):
    """
    Automatically generate categorical visualizations.

    Categorical and boolean columns are detected automatically
    using the column detection engine.

    High-cardinality columns are skipped to prevent unreadable
    visualizations.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to visualize.

    top_n : int, default=15
        Number of top categories displayed in each chart.

    max_categories : int, default=30
        Maximum number of unique categories allowed for plotting.

    Returns
    -------
    dict
        Dictionary containing frequency tables and Matplotlib figures.
    """

    _validate_dataframe(df)

    groups = get_column_groups(df)

    categorical_columns = groups["categorical"]

    boolean_columns = groups["boolean"]

    columns = (
        categorical_columns
        + boolean_columns
    )

    plots = {}

    for column in columns:

        if _is_high_cardinality(
            df,
            column,
            max_categories=max_categories
        ):
            continue

        column_plots = {}

        try:
            column_plots["frequency_table"] = (
                get_frequency_table(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["frequency_table"] = None

        try:
            column_plots["count"] = (
                plot_count_distribution(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["count"] = None

        try:
            column_plots["percentage"] = (
                plot_percentage_distribution(
                    df,
                    column,
                    top_n=top_n
                )
            )
        except (ValueError, TypeError):
            column_plots["percentage"] = None

        plots[column] = column_plots

    return plots

from src.visualization.datetime_analysis import (
    get_datetime_summary,
    get_datetime_frequency_table,
    plot_datetime_frequency,
    plot_datetime_trend,
    generate_datetime_analysis
)


def test_datetime_summary():
    """
    Test datetime summary generation.
    """

    df = pd.DataFrame({
        "joining_date": pd.to_datetime([
            "2024-01-10",
            "2024-02-15",
            "2024-02-20",
            "2025-01-05"
        ])
    })

    result = get_datetime_summary(
        df,
        "joining_date"
    )

    assert result["column"] == "joining_date"

    assert result["valid_values"] == 4

    assert result["missing_values"] == 0

    assert result["unique_dates"] == 4

    assert result["minimum_date"] == pd.Timestamp(
        "2024-01-10"
    )

    assert result["maximum_date"] == pd.Timestamp(
        "2025-01-05"
    )


def test_datetime_frequency_table():
    """
    Test datetime frequency table generation.
    """

    df = pd.DataFrame({
        "joining_date": pd.to_datetime([
            "2024-01-10",
            "2024-01-15",
            "2024-02-20",
            "2024-02-25",
            "2024-02-28"
        ])
    })

    result = get_datetime_frequency_table(
        df,
        "joining_date",
        frequency="month"
    )

    assert list(result.columns) == [
        "month",
        "count"
    ]

    assert len(result) == 2

    assert result.loc[
        result["month"] == 2,
        "count"
    ].iloc[0] == 3


def test_datetime_frequency_plot():
    """
    Test datetime frequency plot generation.
    """

    df = pd.DataFrame({
        "joining_date": pd.to_datetime([
            "2024-01-10",
            "2024-02-15",
            "2024-02-20"
        ])
    })

    fig = plot_datetime_frequency(
        df,
        "joining_date",
        frequency="month"
    )

    assert fig is not None

    plt.close(fig)


def test_datetime_trend_plot():
    """
    Test chronological datetime trend generation.
    """

    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2024-01-01",
            "2024-01-01",
            "2024-01-02",
            "2024-01-03"
        ])
    })

    fig = plot_datetime_trend(
        df,
        "transaction_date"
    )

    assert fig is not None

    plt.close(fig)


def test_generate_datetime_analysis():
    """
    Test automatic datetime analysis.
    """

    df = pd.DataFrame({
        "joining_date": pd.to_datetime([
            "2024-01-10",
            "2024-02-15",
            "2024-02-20",
            "2025-01-05"
        ]),
        "department": [
            "IT",
            "HR",
            "Finance",
            "IT"
        ]
    })

    result = generate_datetime_analysis(
        df
    )

    assert "joining_date" in result

    assert result["joining_date"]["summary"] is not None

    assert result["joining_date"]["year"] is not None

    assert result["joining_date"]["month"] is not None

    assert result["joining_date"]["day_of_week"] is not None

    assert result["joining_date"]["trend"] is not None

    plt.close(
        result["joining_date"]["year"]
    )

    plt.close(
        result["joining_date"]["month"]
    )

    plt.close(
        result["joining_date"]["day_of_week"]
    )

    plt.close(
        result["joining_date"]["trend"]
    )


from src.visualization.bivariate import (
    plot_numeric_scatter,
    plot_numeric_regression,
    calculate_pair_correlation,
    get_group_statistics,
    plot_categorical_numeric_boxplot,
    plot_categorical_numeric_violin,
    generate_numeric_numeric_analysis,
    generate_categorical_numeric_analysis,
    generate_bivariate_analysis
)

def test_numeric_scatter():
    """
    Test numeric-numeric scatter plot generation.
    """

    df = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [25000, 30000, 40000, 50000, 60000]
    })

    fig = plot_numeric_scatter(
        df,
        "age",
        "salary"
    )

    assert fig is not None

    plt.close(fig)


def test_numeric_regression():
    """
    Test numeric regression plot generation.
    """

    df = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [25000, 30000, 40000, 50000, 60000]
    })

    fig = plot_numeric_regression(
        df,
        "age",
        "salary"
    )

    assert fig is not None

    plt.close(fig)


def test_pair_correlation():
    """
    Test correlation calculation between numeric columns.
    """

    df = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [20000, 30000, 40000, 50000, 60000]
    })

    correlation = calculate_pair_correlation(
        df,
        "age",
        "salary"
    )

    assert correlation > 0.99


def test_group_statistics():
    """
    Test grouped statistics between categorical and numeric columns.
    """

    df = pd.DataFrame({
        "department": [
            "IT",
            "IT",
            "HR",
            "HR",
            "Finance"
        ],
        "salary": [
            50000,
            60000,
            40000,
            45000,
            55000
        ]
    })

    result = get_group_statistics(
        df,
        "department",
        "salary"
    )

    assert "department" in result.columns

    assert "mean" in result.columns

    assert "median" in result.columns

    assert len(result) == 3


def test_categorical_numeric_boxplot():
    """
    Test categorical-numeric boxplot generation.
    """

    df = pd.DataFrame({
        "department": [
            "IT",
            "IT",
            "HR",
            "HR",
            "Finance"
        ],
        "salary": [
            50000,
            60000,
            40000,
            45000,
            55000
        ]
    })

    fig = plot_categorical_numeric_boxplot(
        df,
        "department",
        "salary"
    )

    assert fig is not None

    plt.close(fig)


def test_categorical_numeric_violin():
    """
    Test categorical-numeric violin plot generation.
    """

    df = pd.DataFrame({
        "department": [
            "IT",
            "IT",
            "HR",
            "HR",
            "Finance"
        ],
        "salary": [
            50000,
            60000,
            40000,
            45000,
            55000
        ]
    })

    fig = plot_categorical_numeric_violin(
        df,
        "department",
        "salary"
    )

    assert fig is not None

    plt.close(fig)


def test_generate_numeric_numeric_analysis():
    """
    Test automatic numeric-numeric analysis.
    """

    df = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [25000, 30000, 40000, 50000, 60000],
        "experience": [1, 2, 4, 7, 10]
    })

    result = generate_numeric_numeric_analysis(
        df
    )

    assert len(result) == 3

    assert "age__salary" in result

    assert "age__experience" in result

    assert "salary__experience" in result

    for pair_data in result.values():

        if pair_data["scatter"] is not None:
            plt.close(pair_data["scatter"])

        if pair_data["regression"] is not None:
            plt.close(pair_data["regression"])


def test_generate_categorical_numeric_analysis():
    """
    Test automatic categorical-numeric analysis.
    """

    df = pd.DataFrame({
        "department": [
            "IT",
            "IT",
            "HR",
            "HR",
            "Finance"
        ],
        "salary": [
            50000,
            60000,
            40000,
            45000,
            55000
        ]
    })

    result = generate_categorical_numeric_analysis(
        df
    )

    assert "department__salary" in result

    assert (
        result["department__salary"]["statistics"]
        is not None
    )

    assert (
        result["department__salary"]["boxplot"]
        is not None
    )

    assert (
        result["department__salary"]["violin"]
        is not None
    )

    plt.close(
        result["department__salary"]["boxplot"]
    )

    plt.close(
        result["department__salary"]["violin"]
    )


def test_generate_bivariate_analysis():
    """
    Test the complete automated bivariate analysis.
    """

    df = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [25000, 30000, 40000, 50000, 60000],
        "department": [
            "IT",
            "IT",
            "HR",
            "HR",
            "Finance"
        ]
    })

    result = generate_bivariate_analysis(
        df
    )

    assert "numeric_numeric" in result

    assert "categorical_numeric" in result

    assert "age__salary" in (
        result["numeric_numeric"]
    )

    assert "department__age" in (
        result["categorical_numeric"]
    )

    assert "department__salary" in (
        result["categorical_numeric"]
    )

    for pair_data in result["numeric_numeric"].values():

        if pair_data["scatter"] is not None:
            plt.close(pair_data["scatter"])

        if pair_data["regression"] is not None:
            plt.close(pair_data["regression"])

    for pair_data in result["categorical_numeric"].values():

        if pair_data["boxplot"] is not None:
            plt.close(pair_data["boxplot"])

        if pair_data["violin"] is not None:
            plt.close(pair_data["violin"])



from src.visualization.correlation import (
    calculate_correlation_matrix,
    get_strong_correlations,
    plot_correlation_heatmap,
    generate_correlation_analysis
)

from src.visualization.outliers import (
    detect_iqr_outliers,
    detect_zscore_outliers,
    plot_outlier_boxplot,
    generate_outlier_analysis
)

from src.visualization.correlation import (
    calculate_correlation_matrix,
    get_strong_correlations,
    plot_correlation_heatmap,
    generate_correlation_analysis
)

from src.visualization.outliers import (
    detect_iqr_outliers,
    detect_zscore_outliers,
    plot_outlier_boxplot,
    generate_outlier_analysis
)