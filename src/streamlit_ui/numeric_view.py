import streamlit as st

from src.visualization.numeric_plots import plot_numeric


def show_numeric(df,numeric_data):
    """Display numeric analysis and visualizations."""
    st.subheader("🔢 Numeric Analysis")

    if not numeric_data:
        st.info("No numeric columns found.")
        return

    for column,data in numeric_data.items():

        with st.expander(column):

            st.json(data)

            plots=plot_numeric(df,column)

            st.pyplot(plots["histogram"])
            st.pyplot(plots["boxplot"])