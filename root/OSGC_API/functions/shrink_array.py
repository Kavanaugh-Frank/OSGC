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


# use bilinear interpolation
def interpolation(df, num_x_slice, num_y_slice):
    x_resolution, y_resolution = df.shape

    x_percent_spacing = 100 / (num_x_slice - 1) if num_x_slice > 1 else 0
    y_percent_spacing = 100 / (num_y_slice - 1) if num_y_slice > 1 else 0
    
    x_indices = []
    x_indices_decimal = []
    for i in range(num_x_slice - 1):
        index = math.floor(((i * x_percent_spacing) / 100) * (x_resolution - 1))
        x_indices.append(index)

        index_remainder = ((i * x_percent_spacing) / 100) * (x_resolution - 1) % 1
        x_indices_decimal.append(index_remainder)

    x_indices.append(x_resolution - 1)
    x_indices_decimal.append(0)

    y_indices = []
    y_indices_decimal = []
    for i in range(num_y_slice - 1):
        index = math.floor(((i * y_percent_spacing) / 100) * (y_resolution - 1))
        y_indices.append(index)

        index_remainder = ((i * y_percent_spacing) / 100) * (y_resolution - 1) % 1
        y_indices_decimal.append(index_remainder)


    y_indices.append(y_resolution - 1)
    y_indices_decimal.append(0)

    shrunken_array = []
    for x_counter in range(num_x_slice):
        temp_array = []
        for y_counter in range(num_y_slice):
            # f(x,y)=f(0,0)(1−x)(1−y)+f(1,0)x(1−y)+f(0,1)(1−x)y+f(1,1)xy
            x_index = x_indices[x_counter]
            y_index = y_indices[y_counter]

            # since we round down on the indices our current index is the top left of 4 squares
            # so we take the surrounding three tiles to the right and bottom
            top_left_value = df.iat[x_index, y_index] if x_index < x_resolution and y_index < y_resolution else 0
            bottom_right_value = df.iat[x_index + 1, y_index + 1] if x_index < x_resolution - 1 and y_index < y_resolution - 1 else 0
            bottom_left_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 and y_index < y_resolution else 0
            top_right_value = df.iat[x_index, y_index + 1] if x_index < x_resolution and y_index < y_resolution - 1 else 0

            # the decimal values from the calculated index
            x_distance = x_indices_decimal[x_counter]
            y_distance = y_indices_decimal[y_counter]

            # f(0,0)(1−x)(1−y)
            v1 = top_left_value * (1 - x_distance) * (1 - y_distance)
            # f(1,0)x(1−y)
            v2 = top_right_value * x_distance * (1 - y_distance)
            # f(0,1)(1−x)y
            v3 = bottom_left_value * (1 - x_distance) * y_distance
            # f(1,1)xy
            v4 = bottom_right_value * x_distance * y_distance

            # get the final value
            final_value = v1 + v2 + v3 + v4

            temp_array.append(final_value)

        shrunken_array.append(temp_array)

    return pd.DataFrame(shrunken_array)