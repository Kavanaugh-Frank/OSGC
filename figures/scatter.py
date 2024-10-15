import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches

import requests
import pandas as pd
import json

# Define the URL for the API endpoint
url = "http://localhost:8080/process_coordinates"

# Define the data payload to send in the POST request

payload = {
    "upper_lat": 39.5,
    "lower_lat": 39.2,
    "upper_long": -82.5,
    "lower_long": -82.2,
    "num_x_slice": 300,
    "num_y_slice": 300
}

def make_scatter_plot(df):
    df_reverse = df.iloc[::-1]  # Reverse the DataFrame for correct orientation
    plt.figure(figsize=(10, 8))  # Adjust figure size as necessary

    # Create the heatmap
    heatmap = plt.imshow(df_reverse, cmap='viridis', aspect='auto', origin='lower')
    plt.clim(df_reverse.min().min(), df_reverse.max().max())
    plt.colorbar(heatmap, label='Elevation Values')


    # Add contour lines
    # contours = plt.contour(df_reverse, levels=15, cmap='coolwarm', linewidths=0.5)  # Adjust levels as needed
    # plt.clabel(contours, inline=True, fontsize=8, fmt='%.1f')  # Label contour lines

    # Label axes and title
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Figure')
    plt.grid(False)  # Turn off grid for imshow 

    # square = patches.Rectangle((0, df_reverse.shape[0] - 61), 60, 60, linewidth=3, edgecolor='red', facecolor='none')
    # plt.gca().add_patch(square)  # Add the square to the plot

    plt.tight_layout()
    plt.savefig("fig.png")  # Save the figure
    plt.close()  # Close the plot to free memory

# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    response_data = response.json()
    
    # Extract the data and shape from the response
    data_array = json.loads(response_data["data"])  # Load the data string into a list
    shape = response_data["shape"]
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data_array, columns=[f'Column {i}' for i in range(shape[1])])
    
    # Print the DataFrame
    # print(df)
    print("Making the Figure")
    make_scatter_plot(df)
