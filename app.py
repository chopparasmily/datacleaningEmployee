
import streamlit as st
import pandas as pd

from src.pipeline import run_dataframe_pipeline
from src.eda.eda_engine import generate_eda
from src.eda.report import generate_report
from src.streamlit_ui.dashboard import show_dashboard


def load_uploaded_file(uploaded_file):
    """Load an uploaded CSV file into a pandas DataFrame."""
    if uploaded_file is None:
        return None

    return pd.read_csv(uploaded_file)


def main():
    """Run the Employee Data Cleaning and EDA Streamlit application."""
    st.set_page_config(
        page_title="Employee Data Cleaning & EDA",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Employee Data Cleaning & EDA")
    st.markdown(
        "Upload employee data to run the complete "
        "cleaning, validation, EDA, visualization, and reporting pipeline."
    )

    st.sidebar.header("📂 Data Input")

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("Please upload a CSV file from the sidebar.")
        return

    try:
        df = load_uploaded_file(uploaded_file)

        st.subheader("📥 Raw Dataset")
        st.dataframe(df.head(20), width="stretch")

        st.write(
            f"Raw dataset shape: **{df.shape[0]} rows × {df.shape[1]} columns**"
        )

        with st.spinner("Running data cleaning pipeline..."):
            clean_df = run_dataframe_pipeline(df)

        st.success("Data cleaning and validation completed successfully.")

        with st.expander("🧹 Cleaned Dataset Preview"):
            st.dataframe(clean_df.head(20), width="stretch")
            st.write(
                f"Cleaned dataset shape: "
                f"**{clean_df.shape[0]} rows × {clean_df.shape[1]} columns**"
            )

        with st.spinner("Generating EDA analysis..."):
            eda_result = generate_eda(clean_df)

        with st.spinner("Generating EDA report..."):
            report = generate_report(eda_result)

        st.success("EDA analysis completed successfully.")

        show_dashboard(clean_df, report)

    except Exception as error:
        st.error("The application encountered an error.")
        st.exception(error)


if __name__ == "__main__":
    main()
