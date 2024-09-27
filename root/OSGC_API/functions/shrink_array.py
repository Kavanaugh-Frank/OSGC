import math
import pandas as pd

def shrink_dataframe(df, target_size):
    original_height, original_width = df.shape
    
    if original_width <= 30 and original_height <= 30:
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