import matplotlib.pyplot as plt
import seaborn as sns


def plot_outliers(df,column):
    """Create a boxplot for detecting potential outliers."""
    fig,ax=plt.subplots(figsize=(8,4))

    sns.boxplot(
        data=df,
        x=column,
        ax=ax
    )

    ax.set_title(f"{column} Outlier Analysis")

    plt.tight_layout()
    return fig