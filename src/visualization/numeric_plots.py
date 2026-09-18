import matplotlib.pyplot as plt
import seaborn as sns


def plot_histogram(df,column):
    """Create a histogram with KDE for a numeric column."""
    fig,ax=plt.subplots(figsize=(8,5))
    sns.histplot(data=df,x=column,kde=True,ax=ax)
    ax.set_title(f"{column} Distribution")
    plt.tight_layout()
    return fig


def plot_boxplot(df,column):
    """Create a boxplot for a numeric column."""
    fig,ax=plt.subplots(figsize=(8,4))
    sns.boxplot(data=df,x=column,ax=ax)
    ax.set_title(f"{column} Boxplot")
    plt.tight_layout()
    return fig


def plot_numeric(df,column):
    """Create standard plots for a numeric column."""
    return {
        "histogram":plot_histogram(df,column),
        "boxplot":plot_boxplot(df,column)
    }