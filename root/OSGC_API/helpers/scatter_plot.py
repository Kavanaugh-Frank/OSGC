import matplotlib.pyplot as plt

def make_scatter_plot(df):
    """
    Generates and saves a heatmap of the given DataFrame.

    This function takes a DataFrame, reverses its order, and creates a heatmap
    using Matplotlib's imshow function. The heatmap is saved as 'fig.png' in the
    current working directory.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be visualized as a heatmap.

    Returns:
    None
    """
    df_reverse = df.iloc[::-1]
    plt.figure(figsize=(200, 200))
    plt.imshow(df_reverse, cmap='viridis', aspect='auto', origin='lower')
    plt.colorbar(label='Values')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    plt.title('Heatmap of DataFrame')
    plt.grid(False)  # Turn off grid for imshow 
    plt.savefig("fig.png")
    return 