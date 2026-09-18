import streamlit as st

from src.visualization.relationship_plots import (
    plot_scatter,
    plot_regression,
    plot_category_numeric,
    plot_violin
)


def show_bivariate(df,bivariate_data):
    """Display bivariate analysis and visualizations."""
    st.subheader("🔗 Bivariate Analysis")

    numeric_numeric=bivariate_data.get(
        "numeric_numeric",{}
    )

    categorical_numeric=bivariate_data.get(
        "categorical_numeric",{}
    )

    if numeric_numeric:

        st.markdown("### Numeric vs Numeric")

        for name,data in numeric_numeric.items():

            with st.expander(name):

                st.metric(
                    "Correlation",
                    round(data.get("correlation",0),3)
                )

                x_column=data["x_column"]
                y_column=data["y_column"]

                st.pyplot(
                    plot_scatter(
                        df,
                        x_column,
                        y_column
                    )
                )

                st.pyplot(
                    plot_regression(
                        df,
                        x_column,
                        y_column
                    )
                )

    if categorical_numeric:

        st.markdown("### Categorical vs Numeric")

        for name,data in categorical_numeric.items():

            with st.expander(name):

                st.dataframe(
                    data["group_statistics"],
                    width="stretch"
                )

                categorical_column=data["categorical_column"]
                numeric_column=data["numeric_column"]

                st.pyplot(
                    plot_category_numeric(
                        df,
                        categorical_column,
                        numeric_column
                    )
                )

                st.pyplot(
                    plot_violin(
                        df,
                        categorical_column,
                        numeric_column
                    )
                )