import math
import pandas as pd
from helpers.ecef import latlon_to_ecef
from decimal import Decimal

""" These are not used in the final version of the code, but are kept here for reference purposes. """
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


def interpolation(df, num_x_slice, num_y_slice, lat, long, lat_difference, long_distance, point):
    """
    Perform bilinear and linear interpolation on a given dataframe to shrink it to a specified size.
    Parameters:
    df (pd.DataFrame): The input dataframe containing the data to be interpolated.
    num_x_slice (int): The number of slices in the x-direction (latitude).
    num_y_slice (int): The number of slices in the y-direction (longitude).
    lat (float): The starting latitude.
    long (float): The starting longitude.
    lat_difference (float): The total difference in latitude to be covered.
    long_distance (float): The total difference in longitude to be covered.
    Returns:
    pd.DataFrame: A new dataframe containing the interpolated values with columns for X, Y, and Z coordinates.
    Notes:
    - The function first performs bilinear interpolation for all but the bottom row and the right-most column.
    - Linear interpolation is then applied to the bottom row and the right-most column.
    - The bottom-right corner value is handled explicitly.
    - The latitude and longitude for each interpolated point are calculated and converted to ECEF coordinates.
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
    lat_step = lat_difference / (num_x_slice - 1)  # Latitude step size
    long_step = long_distance / (num_y_slice - 1)  # Longitude step size

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

            # Bilinear interpolation calculation for elevation
            v1 = top_left_value * (1 - x_distance) * (1 - y_distance)
            v2 = top_right_value * x_distance * (1 - y_distance)
            v3 = bottom_left_value * (1 - x_distance) * y_distance
            v4 = bottom_right_value * x_distance * y_distance

            # Final interpolated elevation value
            final_value = v1 + v2 + v3 + v4

            # Calculate latitude and longitude for the current point
            current_lat = lat - (x_counter * lat_step)  # Using corrected lat_step
            current_long = long + (y_counter * long_step)  # Using corrected long_step

            X, Y, Z = latlon_to_ecef(current_lat, current_long, final_value)
            # Convert the point to ECEF coordinates
            point_ecef = latlon_to_ecef(point[0], point[1], point[2])
            # Apply the offset point using Decimal for precision
            # X = Decimal(point_ecef[0]) - Decimal(X)
            # Y = Decimal(point_ecef[1]) - Decimal(Y)
            # Z = Decimal(point_ecef[2]) - Decimal(Z)
            X = Decimal(X) - Decimal(point_ecef[0])
            Y = Decimal(Y) - Decimal(point_ecef[1])
            Z = Decimal(Z) - Decimal(point_ecef[2])
            # Append the array [lat, long, elevation]
            temp_array.append([X, Y, Z])

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
        final_value = left_value * (1 - y_distance) + right_value * y_distance

        # Calculate latitude and longitude for the current point
        current_lat = lat - ((num_x_slice - 1) * lat_step)
        current_long = long + (y_counter * long_step)

        X, Y, Z = latlon_to_ecef(current_lat, current_long, final_value)
        # Convert the point to ECEF coordinates
        point_ecef = latlon_to_ecef(point[0], point[1], point[2])
        # Apply the offset point using Decimal for precision
        # X = Decimal(point_ecef[0]) - Decimal(X)
        # Y = Decimal(point_ecef[1]) - Decimal(Y)
        # Z = Decimal(point_ecef[2]) - Decimal(Z)
        X = Decimal(X) - Decimal(point_ecef[0])
        Y = Decimal(Y) - Decimal(point_ecef[1])
        Z = Decimal(Z) - Decimal(point_ecef[2])
        bottom_row.append([X, Y, Z])

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
        final_value = top_value * (1 - x_distance) + bottom_value * x_distance

        # Calculate latitude and longitude for the current point
        current_lat = lat - (x_counter * lat_step)
        current_long = long + ((num_y_slice - 1) * long_step)

        X, Y, Z = latlon_to_ecef(current_lat, current_long, final_value)
        # Convert the point to ECEF coordinates
        point_ecef = latlon_to_ecef(point[0], point[1], point[2])
        # Apply the offset point using Decimal for precision
        # X = Decimal(point_ecef[0]) - Decimal(X)
        # Y = Decimal(point_ecef[1]) - Decimal(Y)
        # Z = Decimal(point_ecef[2]) - Decimal(Z)
        X = Decimal(X) - Decimal(point_ecef[0])
        Y = Decimal(Y) - Decimal(point_ecef[1])
        Z = Decimal(Z) - Decimal(point_ecef[2])
        # Append the array [lat, long, elevation]
        shrunken_array[x_counter].append([X, Y, Z])

    # Handle the bottom-right corner value explicitly
    bottom_right_value = df.iat[x_indices[-1], y_indices[-1]]
    current_lat = lat - ((num_x_slice - 1) * lat_step)
    current_long = long + ((num_y_slice - 1) * long_step)

    X, Y, Z = latlon_to_ecef(current_lat, current_long, bottom_right_value)
    # Convert the point to ECEF coordinates
    point_ecef = latlon_to_ecef(point[0], point[1], point[2])
    # Apply the offset point using Decimal for precision
    # X = Decimal(point_ecef[0]) - Decimal(X)
    # Y = Decimal(point_ecef[1]) - Decimal(Y)
    # Z = Decimal(point_ecef[2]) - Decimal(Z)
    X = Decimal(X) - Decimal(point_ecef[0])
    Y = Decimal(Y) - Decimal(point_ecef[1])
    Z = Decimal(Z) - Decimal(point_ecef[2])
    shrunken_array[-1].append([X, Y, Z])

    # Return the new dataframe with lat, long, and elevation
    return pd.DataFrame(shrunken_array)
