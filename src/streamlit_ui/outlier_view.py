import streamlit as st

from src.visualization.outlier_plots import plot_outliers


def show_outliers(df,outlier_data):
    """Display outlier analysis and boxplots."""
    st.subheader("🚨 Outlier Analysis")

    if not outlier_data:
        st.info("No numeric columns found.")
        return

    for column,data in outlier_data.items():

        with st.expander(column):

            col1,col2=st.columns(2)

            col1.metric(
                "IQR Outliers",
                data.get("iqr_count",0)
            )

            col2.metric(
                "Z-Score Outliers",
                data.get("zscore_count",0)
            )

            st.pyplot(
                plot_outliers(df,column)
            )