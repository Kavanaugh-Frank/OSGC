import matplotlib.pyplot as plt
import matplotlib

"""
Takes in a DF and then creates a scatter plot that should recreate the TIFF
file in scatter plot form
"""


def make_scatter_plot(df):
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