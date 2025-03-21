import math
import pandas as pd
from main_function.ecef import latlon_to_ecef  # Ensure this import is correct and the function exists
from decimal import Decimal

def interpolation(df, num_x_slice, num_y_slice, lat, long, lat_difference, long_difference, point):
    """
    Perform interpolation on a DataFrame to shrink its size and convert latitude and longitude to ECEF coordinates.
    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be interpolated.
        num_x_slice (int): The number of slices along the x-axis.
        num_y_slice (int): The number of slices along the y-axis.
        lat (float): The starting latitude.
        long (float): The starting longitude.
        lat_difference (float): The total difference in latitude to cover.
        long_difference (float): The total difference in longitude to cover.
        point (tuple): A tuple containing the reference point (latitude, longitude, altitude).
    Returns:
        pd.DataFrame: A DataFrame containing the interpolated and shrunken array with ECEF coordinates.
    """
    x_resolution, y_resolution = df.shape

    if x_resolution < 2 or y_resolution < 2:
        raise ValueError("DataFrame must have at least two rows and columns for interpolation.")

    point_ecef = latlon_to_ecef(point[0], point[1], point[2])
    print(f"Point ECEF: {point_ecef}")
    
    x_percent_spacing = 100 / max(num_x_slice - 1, 1)
    y_percent_spacing = 100 / max(num_y_slice - 1, 1)

    x_indices, x_indices_decimal = [], []
    for i in range(num_x_slice):
        index = min(math.floor((i * x_percent_spacing / 100) * (x_resolution - 1)), x_resolution - 1)
        x_indices.append(index)
        x_indices_decimal.append(((i * x_percent_spacing) / 100) * (x_resolution - 1) % 1)

    y_indices, y_indices_decimal = [], []
    for i in range(num_y_slice):
        index = min(math.floor((i * y_percent_spacing / 100) * (y_resolution - 1)), y_resolution - 1)
        y_indices.append(index)
        y_indices_decimal.append(((i * y_percent_spacing) / 100) * (y_resolution - 1) % 1)

    lat_step = lat_difference / max(num_x_slice - 1, 1)
    long_step = long_difference / max(num_y_slice - 1, 1)

    shrunken_array = []
    latlon_cache = {}
    
    for x_counter in range(num_x_slice):
        temp_array = []
        for y_counter in range(num_y_slice):
            x_index, y_index = x_indices[x_counter], y_indices[y_counter]

            # Debugging index and data values
            print(f"\nProcessing x_index: {x_index}, y_index: {y_index}")

            top_left_value = df.iat[x_index, y_index]
            bottom_right_value = df.iat[min(x_index + 1, x_resolution - 1), min(y_index + 1, y_resolution - 1)]
            bottom_left_value = df.iat[min(x_index + 1, x_resolution - 1), y_index]
            top_right_value = df.iat[x_index, min(y_index + 1, y_resolution - 1)]

            # Print values for interpolation debugging
            print(f"Top Left: {top_left_value}, Top Right: {top_right_value}")
            print(f"Bottom Left: {bottom_left_value}, Bottom Right: {bottom_right_value}")

            x_distance, y_distance = x_indices_decimal[x_counter], y_indices_decimal[y_counter]

            final_value = (
                top_left_value * (1 - x_distance) * (1 - y_distance) +
                top_right_value * x_distance * (1 - y_distance) +
                bottom_left_value * (1 - x_distance) * y_distance +
                bottom_right_value * x_distance * y_distance
            )

            current_lat = lat - (x_counter * lat_step)
            current_long = long + (y_counter * long_step)

            if (current_lat, current_long, final_value) not in latlon_cache:
                latlon_cache[(current_lat, current_long, final_value)] = latlon_to_ecef(current_lat, current_long, final_value)
            X, Y, Z = latlon_cache[(current_lat, current_long, final_value)]
            X, Y, Z = Decimal(X) - Decimal(point_ecef[0]), Decimal(Y) - Decimal(point_ecef[1]), Decimal(Z) - Decimal(point_ecef[2])

            # Print Z values for debugging
            print(f"Calculated Z: {Z}")

            temp_array.append([X, Y, Z])
        shrunken_array.append(temp_array)

    return pd.DataFrame(shrunken_array)

