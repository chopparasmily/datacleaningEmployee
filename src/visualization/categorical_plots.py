import matplotlib.pyplot as plt
import seaborn as sns


def plot_count(df,column):
    """Create a count plot for a categorical column."""
    fig,ax=plt.subplots(figsize=(8,5))

    order=df[column].value_counts().head(10).index

    sns.countplot(
        data=df,
        x=column,
        order=order,
        ax=ax
    )

    ax.set_title(f"{column} Frequency")
    ax.tick_params(axis="x",rotation=45)

    plt.tight_layout()
    return fig


def plot_percentage(df,column):
    """Create a percentage bar plot for a categorical column."""
    values=df[column].value_counts(normalize=True).head(10)*100

    fig,ax=plt.subplots(figsize=(8,5))

    values.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_title(f"{column} Percentage")
    ax.set_xlabel("Percentage")

    plt.tight_layout()
    return fig


def plot_categorical(df,column):
    """Create standard plots for a categorical column."""
    return {
        "count":plot_count(df,column),
        "percentage":plot_percentage(df,column)
    }