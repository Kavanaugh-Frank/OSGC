import math
import pandas as pd

def shrink_dataframe(df, target_size):
    original_height, original_width = df.shape
    
    if original_width <= target_size and original_height <= target_size:
        return df


    step_size_height = original_height / target_size
    step_size_width = original_width / target_size

    selected_row_indices = []
    selected_col_indices = []

    # going through each step and calculating the new index
    for i in range(target_size):
        row_index = int(math.floor(step_size_height * i))
        selected_row_indices.append(row_index)

    for i in range(target_size):
        col_index = int(math.floor(step_size_width * i))
        selected_col_indices.append(col_index)

    # Checks each new index to make sure that it does not go over the size of the original array
    for idx in range(len(selected_row_indices)):
        selected_row_indices[idx] = min(selected_row_indices[idx], original_height - 1)

    for idx in range(len(selected_col_indices)):
        selected_col_indices[idx] = min(selected_col_indices[idx], original_width - 1)

    # actually making a new DF with only those selected data points
    shrunk_df = df.iloc[selected_row_indices, selected_col_indices]

    return shrunk_df


def nearest_neighbor(df, num_x_slice, num_y_slice):
    # x_slice is the number of horizontal pixels taken from the larger array and made to the smaller 
    # y_slice is the number of vertical pixels taken from the larger array and made to the smaller

    x_resolution, y_resolution = df.shape

    x_percent_spacing = 100 / (num_x_slice - 1)
    y_percent_spacing = 100 / (num_y_slice - 1)

    x_indices = []
    for i in range(0, num_x_slice - 1):
        index = round(((i * x_percent_spacing)/100) * (x_resolution-1)) # nearest int
        x_indices.append(index)
    x_indices.append((x_resolution - 1)) # add the last index

    y_indices = []
    for i in range(0, num_y_slice - 1):
        index = round(((i * y_percent_spacing)/100) * (y_resolution-1)) # nearest int
        y_indices.append(index)
    y_indices.append(y_resolution - 1) # add the last index

    sliced_df = df.iloc[x_indices, y_indices]

    return sliced_df

    

        