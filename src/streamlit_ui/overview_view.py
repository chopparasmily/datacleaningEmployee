import streamlit as st


def show_overview(report):
    """Display dataset overview."""
    summary=report.get("summary",{})

    st.subheader("📊 Dataset Overview")

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Rows",summary.get("rows",0))
    col2.metric("Columns",summary.get("columns",0))
    col3.metric("Missing Values",summary.get("missing_values",0))
    col4.metric("Duplicates",summary.get("duplicate_rows",0))

    st.markdown("### Column Profile")

    profile=report.get("column_profile")

    if profile is not None:
        st.dataframe(profile,width="stretch")