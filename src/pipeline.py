from .reader import read_file
from .profiler import profile_data
from .cleaner import clean_data
from .string_cleaner import clean_strings
from .numeric_cleaner import clean_numbers
from .date_cleaner import clean_dates
from .validator import validate_data
from .transformer import transform_data
from .exporter import export_data


def run_dataframe_pipeline(
    df,
    employee_ids=None,
    department_ids=None,
):
    """
    Run the complete cleaning pipeline on an in-memory DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    employee_ids : iterable, optional
        Valid employee identifiers.
    department_ids : iterable, optional
        Valid department identifiers.

    Returns
    -------
    pandas.DataFrame
        Cleaned, validated and transformed DataFrame.
    """
    if df is None:
        raise ValueError("df cannot be None.")

    df = df.copy()

    df = clean_data(df)

    df = clean_strings(df)

    df = clean_numbers(df)

    df = clean_dates(df)

    df = validate_data(
        df,
        employee_ids,
        department_ids,
    )

    df = transform_data(df)

    return df


def run_pipeline(
    input_path,
    output_path,
    rejected_path=None,
    employee_ids=None,
    department_ids=None,
):
    """
    Run the complete cleaning pipeline for one dataset.

    Parameters
    ----------
    input_path : str
        Input CSV path.
    output_path : str
        Output cleaned CSV path.
    rejected_path : str, optional
        Output rejected CSV path.
    employee_ids : iterable, optional
        Valid employee identifiers.
    department_ids : iterable, optional
        Valid department identifiers.

    Returns
    -------
    pandas.DataFrame
        Processed DataFrame.
    """
    df = read_file(input_path)

    print("\n===== RAW DATA =====")

    profile_data(df)

    df = run_dataframe_pipeline(
        df,
        employee_ids=employee_ids,
        department_ids=department_ids,
    )

    export_data(
        df,
        output_path,
        rejected_path,
    )

    return df