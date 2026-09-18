import streamlit as st

from src.visualization.datetime_plots import plot_datetime


def show_datetime(df,datetime_data):
    """Display datetime analysis and visualizations."""
    st.subheader("📅 Datetime Analysis")

    if not datetime_data:
        st.info("No datetime columns found.")
        return

    for column,data in datetime_data.items():

        with st.expander(column):

            st.write(
                "Start Date:",
                data.get("start_date")
            )

            st.write(
                "End Date:",
                data.get("end_date")
            )

            if data.get("year") is not None:
                st.dataframe(
                    data["year"],
                    width="stretch"
                )

            if data.get("month") is not None:
                st.dataframe(
                    data["month"],
                    width="stretch"
                )

            plots=plot_datetime(df,column)

            st.pyplot(plots["year"])
            st.pyplot(plots["month"])