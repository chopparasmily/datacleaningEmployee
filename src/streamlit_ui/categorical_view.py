import streamlit as st

from src.visualization.categorical_plots import plot_categorical


def show_categorical(df,categorical_data):
    """Display categorical analysis and visualizations."""
    st.subheader("🏷️ Categorical Analysis")

    if not categorical_data:
        st.info("No categorical columns found.")
        return

    for column,data in categorical_data.items():

        with st.expander(column):

            table=data.get("frequency_table")

            if table is not None:
                st.dataframe(table,width="stretch")

            plots=plot_categorical(df,column)

            st.pyplot(plots["count"])
            st.pyplot(plots["percentage"])