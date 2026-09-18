import matplotlib.pyplot as plt
import seaborn as sns


def plot_scatter(df,x_column,y_column):
    """Create a scatter plot for two numeric columns."""
    fig,ax=plt.subplots(figsize=(8,5))

    sns.scatterplot(
        data=df,
        x=x_column,
        y=y_column,
        ax=ax
    )

    ax.set_title(f"{x_column} vs {y_column}")

    plt.tight_layout()
    return fig


def plot_regression(df,x_column,y_column):
    """Create a regression plot for two numeric columns."""
    fig,ax=plt.subplots(figsize=(8,5))

    sns.regplot(
        data=df,
        x=x_column,
        y=y_column,
        ax=ax
    )

    ax.set_title(f"{x_column} vs {y_column}")

    plt.tight_layout()
    return fig


def plot_category_numeric(df,categorical_column,numeric_column):
    """Create a boxplot for categorical versus numeric data."""
    fig,ax=plt.subplots(figsize=(8,5))

    sns.boxplot(
        data=df,
        x=categorical_column,
        y=numeric_column,
        ax=ax
    )

    ax.set_title(
        f"{numeric_column} by {categorical_column}"
    )

    ax.tick_params(axis="x",rotation=45)

    plt.tight_layout()
    return fig


def plot_violin(df,categorical_column,numeric_column):
    """Create a violin plot for categorical versus numeric data."""
    fig,ax=plt.subplots(figsize=(8,5))

    sns.violinplot(
        data=df,
        x=categorical_column,
        y=numeric_column,
        ax=ax
    )

    ax.set_title(
        f"{numeric_column} by {categorical_column}"
    )

    ax.tick_params(axis="x",rotation=45)

    plt.tight_layout()
    return fig