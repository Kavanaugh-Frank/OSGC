import math
import pandas as pd

"""
    Reduces the size of a DataFrame by selecting a subset of rows and columns
    based on the desired `target_size`. It calculates step sizes to pick rows and
    columns that are evenly spaced across the original DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be shrunk.
    target_size (int): The desired number of rows and columns for the resulting DataFrame.

    Returns:
    pd.DataFrame: A new DataFrame with the selected rows and columns. If the original
                  DataFrame is smaller or equal to the `target_size`, the original
                  DataFrame is returned.
"""
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

"""
    Reduces the size of a DataFrame using the nearest neighbor method. The method
    selects rows and columns based on the specified number of slices, choosing indices
    that best match the spacing between slices.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be sliced.
    num_x_slice (int): The number of slices (or columns) desired in the resulting DataFrame.
    num_y_slice (int): The number of slices (or rows) desired in the resulting DataFrame.

    Returns:
    pd.DataFrame: A new DataFrame with selected rows and columns based on nearest neighbor
                  slicing.
"""
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

# def interpolation(df, num_x_slice, num_y_slice):
#     x_resolution, y_resolution = df.shape

#     x_percent_spacing = 100 / (num_x_slice - 1) if num_x_slice > 1 else 0
#     y_percent_spacing = 100 / (num_y_slice - 1) if num_y_slice > 1 else 0
    
#     x_indices = []
#     x_indices_decimal = []
#     for i in range(num_x_slice):
#         index = min(math.floor((i * x_percent_spacing / 100) * (x_resolution - 1)), x_resolution - 1)
#         x_indices.append(index)

#         index_remainder = ((i * x_percent_spacing) / 100) * (x_resolution - 1) % 1
#         x_indices_decimal.append(index_remainder)

#     y_indices = []
#     y_indices_decimal = []
#     for i in range(num_y_slice):
#         index = min(math.floor((i * y_percent_spacing / 100) * (y_resolution - 1)), y_resolution - 1)
#         y_indices.append(index)

#         index_remainder = ((i * y_percent_spacing) / 100) * (y_resolution - 1) % 1
#         y_indices_decimal.append(index_remainder)

    # shrunken_array = []
    # for x_counter in range(num_x_slice - 1):
    #     temp_array = []
    #     for y_counter in range(num_y_slice - 1):
    #         x_index = x_indices[x_counter]
    #         y_index = y_indices[y_counter]

    #         # Initialize values
    #         top_left_value = df.iat[x_index, y_index] if x_index < x_resolution and y_index < y_resolution else 0
    #         bottom_right_value = df.iat[x_index + 1, y_index + 1] if x_index < x_resolution - 1 and y_index < y_resolution - 1 else 0
    #         bottom_left_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 and y_index < y_resolution else 0
    #         top_right_value = df.iat[x_index, y_index + 1] if x_index < x_resolution and y_index < y_resolution - 1 else 0

    #         # The decimal values from the calculated index
    #         x_distance = x_indices_decimal[x_counter]
    #         y_distance = y_indices_decimal[y_counter]

    #         # Interpolation calculation
    #         v1 = top_left_value * (1 - x_distance) * (1 - y_distance)
    #         v2 = top_right_value * x_distance * (1 - y_distance)
    #         v3 = bottom_left_value * (1 - x_distance) * y_distance
    #         v4 = bottom_right_value * x_distance * y_distance

    #         # Final value
    #         final_value = v1 + v2 + v3 + v4
    #         temp_array.append(final_value)

    #     shrunken_array.append(temp_array)

    # return pd.DataFrame(shrunken_array)
# def interpolation(df, num_x_slice, num_y_slice):
#     # Get the resolution of the dataframe (number of rows and columns)
#     x_resolution, y_resolution = df.shape

#     # Calculate spacing percentages for x and y
#     x_percent_spacing = 100 / (num_x_slice - 1) if num_x_slice > 1 else 0
#     y_percent_spacing = 100 / (num_y_slice - 1) if num_y_slice > 1 else 0

#     # Generate index positions and decimal remainders for x and y
#     x_indices = []
#     x_indices_decimal = []
#     for i in range(num_x_slice):
#         index = min(math.floor((i * x_percent_spacing / 100) * (x_resolution - 1)), x_resolution - 1)
#         x_indices.append(index)
#         index_remainder = ((i * x_percent_spacing) / 100) * (x_resolution - 1) % 1
#         x_indices_decimal.append(index_remainder)

#     y_indices = []
#     y_indices_decimal = []
#     for i in range(num_y_slice):
#         index = min(math.floor((i * y_percent_spacing / 100) * (y_resolution - 1)), y_resolution - 1)
#         y_indices.append(index)
#         index_remainder = ((i * y_percent_spacing) / 100) * (y_resolution - 1) % 1
#         y_indices_decimal.append(index_remainder)

#     # Step 1: Bilinear interpolation for all but the bottom row and the right-most column
#     shrunken_array = []
#     for x_counter in range(num_x_slice - 1):
#         temp_array = []
#         for y_counter in range(num_y_slice - 1):
#             x_index = x_indices[x_counter]
#             y_index = y_indices[y_counter]

#             # Initialize values for bilinear interpolation
#             top_left_value = df.iat[x_index, y_index] if x_index < x_resolution and y_index < y_resolution else 0
#             bottom_right_value = df.iat[x_index + 1, y_index + 1] if x_index < x_resolution - 1 and y_index < y_resolution - 1 else 0
#             bottom_left_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 and y_index < y_resolution else 0
#             top_right_value = df.iat[x_index, y_index + 1] if x_index < x_resolution and y_index < y_resolution - 1 else 0

#             # The decimal values from the calculated index
#             x_distance = x_indices_decimal[x_counter]
#             y_distance = y_indices_decimal[y_counter]

#             # Bilinear interpolation calculation
#             v1 = top_left_value * (1 - x_distance) * (1 - y_distance)
#             v2 = top_right_value * x_distance * (1 - y_distance)
#             v3 = bottom_left_value * (1 - x_distance) * y_distance
#             v4 = bottom_right_value * x_distance * y_distance

#             # Final value with bilinear interpolation
#             final_value = v1 + v2 + v3 + v4
#             temp_array.append(final_value)

#         shrunken_array.append(temp_array)

#     # Step 2: Handle linear interpolation for the bottom row
#     bottom_row = []
#     for y_counter in range(num_y_slice - 1):
#         x_index = x_indices[-1]  # Last x index for the bottom row
#         y_index = y_indices[y_counter]

#         # Linear interpolation between the bottom-left and bottom-right values
#         left_value = df.iat[x_index, y_index]
#         right_value = df.iat[x_index, y_index + 1] if y_index < y_resolution - 1 else left_value
#         y_distance = y_indices_decimal[y_counter]
#         final_value = left_value * (1 - y_distance) + right_value * y_distance
#         bottom_row.append(final_value)

#     # Append the bottom row to the shrunken array
#     shrunken_array.append(bottom_row)

#     # Step 3: Handle linear interpolation for the right-most column
#     for x_counter in range(num_x_slice - 1):
#         x_index = x_indices[x_counter]
#         y_index = y_indices[-1]  # Last y index for the right-most column

#         # Linear interpolation between the top-right and bottom-right values
#         top_value = df.iat[x_index, y_index]
#         bottom_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 else top_value
#         x_distance = x_indices_decimal[x_counter]
#         final_value = top_value * (1 - x_distance) + bottom_value * x_distance

#         # Append the interpolated value to the last row in the shrunken array
#         shrunken_array[x_counter].append(final_value)

#     # Handle the bottom-right corner value explicitly
#     bottom_right_value = df.iat[x_indices[-1], y_indices[-1]]
#     shrunken_array[-1].append(bottom_right_value)

#     # Return the new dataframe
#     return pd.DataFrame(shrunken_array)
def interpolation(df, num_x_slice, num_y_slice):
    """ using bilinear and linear interpolation, return a shrunken DF that represetns the changes in elevtaion of the larger dataset

    Args:
        df ([float, float, float]): The full DF of the dataset to by shrunk
        num_x_slice (int): number of elements to represent the X coordinate
        num_y_slice (int): number of elements to represent the Y coordinate

    Returns:
        DF([float, float, float]): 2D Array where each element is an array of 3 points [X,Y,Z]
    """
    # Get the resolution of the dataframe (number of rows and columns)
    x_resolution, y_resolution = df.shape

    # Calculate spacing percentages for x and y
    x_percent_spacing = 100 / (num_x_slice - 1) if num_x_slice > 1 else 0
    y_percent_spacing = 100 / (num_y_slice - 1) if num_y_slice > 1 else 0

    # Generate index positions and decimal remainders for x and y
    x_indices = []
    x_indices_decimal = []
    for i in range(num_x_slice):
        index = min(math.floor((i * x_percent_spacing / 100) * (x_resolution - 1)), x_resolution - 1)
        x_indices.append(index)
        index_remainder = ((i * x_percent_spacing) / 100) * (x_resolution - 1) % 1
        x_indices_decimal.append(index_remainder)

    y_indices = []
    y_indices_decimal = []
    for i in range(num_y_slice):
        index = min(math.floor((i * y_percent_spacing / 100) * (y_resolution - 1)), y_resolution - 1)
        y_indices.append(index)
        index_remainder = ((i * y_percent_spacing) / 100) * (y_resolution - 1) % 1
        y_indices_decimal.append(index_remainder)

    # Step 1: Bilinear interpolation for all but the bottom row and the right-most column
    shrunken_array = []
    for x_counter in range(num_x_slice - 1):
        temp_array = []
        for y_counter in range(num_y_slice - 1):
            x_index = x_indices[x_counter]
            y_index = y_indices[y_counter]

            # Initialize values for bilinear interpolation
            top_left_value = df.iat[x_index, y_index] if x_index < x_resolution and y_index < y_resolution else 0
            bottom_right_value = df.iat[x_index + 1, y_index + 1] if x_index < x_resolution - 1 and y_index < y_resolution - 1 else 0
            bottom_left_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 and y_index < y_resolution else 0
            top_right_value = df.iat[x_index, y_index + 1] if x_index < x_resolution and y_index < y_resolution - 1 else 0

            # The decimal values from the calculated index
            x_distance = x_indices_decimal[x_counter]
            y_distance = y_indices_decimal[y_counter]

            # Bilinear interpolation calculation
            v1 = top_left_value * (1 - x_distance) * (1 - y_distance)
            v2 = top_right_value * x_distance * (1 - y_distance)
            v3 = bottom_left_value * (1 - x_distance) * y_distance
            v4 = bottom_right_value * x_distance * y_distance

            # Final value with bilinear interpolation (z value)
            z_value = v1 + v2 + v3 + v4

            # Store the [x, y, z] value at this point
            exact_x = x_index + x_distance
            exact_y = y_index + y_distance
            temp_array.append([exact_x, exact_y, z_value])

        shrunken_array.append(temp_array)

    # Step 2: Handle linear interpolation for the bottom row
    bottom_row = []
    for y_counter in range(num_y_slice - 1):
        x_index = x_indices[-1]  # Last x index for the bottom row
        y_index = y_indices[y_counter]

        # Linear interpolation between the bottom-left and bottom-right values
        left_value = df.iat[x_index, y_index]
        right_value = df.iat[x_index, y_index + 1] if y_index < y_resolution - 1 else left_value
        y_distance = y_indices_decimal[y_counter]
        z_value = left_value * (1 - y_distance) + right_value * y_distance

        # Store the [x, y, z] value for the bottom row
        exact_x = x_index
        exact_y = y_index + y_distance
        bottom_row.append([exact_x, exact_y, z_value])

    # Append the bottom row to the shrunken array
    shrunken_array.append(bottom_row)

    # Step 3: Handle linear interpolation for the right-most column
    for x_counter in range(num_x_slice - 1):
        x_index = x_indices[x_counter]
        y_index = y_indices[-1]  # Last y index for the right-most column

        # Linear interpolation between the top-right and bottom-right values
        top_value = df.iat[x_index, y_index]
        bottom_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 else top_value
        x_distance = x_indices_decimal[x_counter]
        z_value = top_value * (1 - x_distance) + bottom_value * x_distance

        # Append the [x, y, z] value to the right-most column in the shrunken array
        exact_x = x_index + x_distance
        exact_y = y_index
        shrunken_array[x_counter].append([exact_x, exact_y, z_value])

    # Handle the bottom-right corner value explicitly
    bottom_right_value = df.iat[x_indices[-1], y_indices[-1]]
    shrunken_array[-1].append([x_indices[-1], y_indices[-1], bottom_right_value])

    # Return the new dataframe with [x, y, z] arrays
    return pd.DataFrame(shrunken_array)

