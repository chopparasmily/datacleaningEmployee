import streamlit as st

from src.streamlit_ui.overview_view import show_overview
from src.streamlit_ui.numeric_view import show_numeric
from src.streamlit_ui.categorical_view import show_categorical
from src.streamlit_ui.datetime_view import show_datetime
from src.streamlit_ui.bivariate_view import show_bivariate
from src.streamlit_ui.correlation_view import show_correlation
from src.streamlit_ui.outlier_view import show_outliers


def show_dashboard(df,report):
    """Display the complete EDA dashboard."""
    show_overview(report)

    st.divider()

    show_numeric(
        df,
        report.get("numeric",{})
    )

    st.divider()

    show_categorical(
        df,
        report.get("categorical",{})
    )

    st.divider()

    show_datetime(
        df,
        report.get("datetime",{})
    )

    st.divider()

    show_bivariate(
        df,
        report.get("bivariate",{})
    )

    st.divider()

    show_correlation(
        report.get("correlation",{})
    )

    st.divider()

    show_outliers(
        df,
        report.get("outliers",{})
    )

    st.divider()

    show_insights(report)


def show_insights(report):
    """Display automatically generated data insights."""
    st.subheader("💡 Data Insights")

    insights=report.get("insights",[])

    if not insights:
        st.info("No automatic insights generated.")
        return

    for insight in insights:
        st.write(f"• {insight}")