import matplotlib.pyplot as plt
import seaborn as sns


def plot_correlation_heatmap(matrix):
    """Create a correlation heatmap."""
    fig,ax=plt.subplots(figsize=(9,6))

    sns.heatmap(
        matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    plt.tight_layout()
    return fig