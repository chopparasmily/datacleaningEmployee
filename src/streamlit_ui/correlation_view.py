import streamlit as st

from src.visualization.correlation_plots import (
    plot_correlation_heatmap
)


def show_correlation(correlation_data):
    """Display correlation analysis."""
    st.subheader("📈 Correlation Analysis")

    matrix=correlation_data.get("matrix")

    if matrix is None or matrix.empty:
        st.info("Not enough numeric columns for correlation analysis.")
        return

    st.write(
        "Method:",
        correlation_data.get("method","pearson")
    )

    st.write(
        "Threshold:",
        correlation_data.get("threshold",0.7)
    )

    st.dataframe(
        matrix,
        width="stretch"
    )

    st.pyplot(
        plot_correlation_heatmap(matrix)
    )

    st.markdown("### Strong Correlations")

    strong=correlation_data.get(
        "strong_correlations",[]
    )

    if strong:
        st.dataframe(
            strong,
            width="stretch"
        )
    else:
        st.info("No strong correlations detected.")