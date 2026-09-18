import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_year(df,column):
    """Create a year frequency plot."""
    series=pd.to_datetime(
        df[column],
        errors="coerce",
        format="mixed"
    ).dropna()

    counts=series.dt.year.value_counts().sort_index()

    fig,ax=plt.subplots(figsize=(8,5))
    sns.barplot(x=counts.index,y=counts.values,ax=ax)

    ax.set_title(f"{column} by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")

    plt.tight_layout()
    return fig


def plot_month(df,column):
    """Create a month frequency plot."""
    series=pd.to_datetime(
        df[column],
        errors="coerce",
        format="mixed"
    ).dropna()

    counts=series.dt.month.value_counts().sort_index()

    fig,ax=plt.subplots(figsize=(8,5))
    sns.barplot(x=counts.index,y=counts.values,ax=ax)

    ax.set_title(f"{column} by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")

    plt.tight_layout()
    return fig


def plot_datetime(df,column):
    """Create standard datetime plots."""
    return {
        "year":plot_year(df,column),
        "month":plot_month(df,column)
    }