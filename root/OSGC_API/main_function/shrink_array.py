import math
import pandas as pd
from main_function.ecef import latlon_to_ecef
from decimal import Decimal

def calculate_offset(point_ecef, X, Y, Z):
    return Decimal(X) - Decimal(point_ecef[0]), Decimal(Y) - Decimal(point_ecef[1]), Decimal(Z) - Decimal(point_ecef[2])

def interpolation(df, num_x_slice, num_y_slice, lat, long, lat_difference, long_distance, point):
    x_resolution, y_resolution = df.shape

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
    long_step = long_distance / max(num_y_slice - 1, 1)

    shrunken_array = []
    for x_counter in range(num_x_slice):
        temp_array = []
        for y_counter in range(num_y_slice):
            x_index, y_index = x_indices[x_counter], y_indices[y_counter]

            # Debugging index and data values
            print(f"\nProcessing x_index: {x_index}, y_index: {y_index}")

            top_left_value = df.iat[x_index, y_index]
            bottom_right_value = df.iat[x_index + 1, y_index + 1] if x_index < x_resolution - 1 and y_index < y_resolution - 1 else top_left_value
            bottom_left_value = df.iat[x_index + 1, y_index] if x_index < x_resolution - 1 else top_left_value
            top_right_value = df.iat[x_index, y_index + 1] if y_index < y_resolution - 1 else top_left_value

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

            X, Y, Z = latlon_to_ecef(current_lat, current_long, final_value)
            X, Y, Z = calculate_offset(point_ecef, X, Y, Z)

            # Print Z values for debugging
            print(f"Calculated Z: {Z}")

            temp_array.append([X, Y, Z])
        shrunken_array.append(temp_array)

    return pd.DataFrame(shrunken_array)

