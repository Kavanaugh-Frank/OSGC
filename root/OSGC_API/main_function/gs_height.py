def get_gs_height(upper_lat, upper_long, lower_lat, lower_long, df, gs_lat, gs_long):
    lat_step = (upper_lat - lower_lat) / (df.shape[0] - 1)
    long_step = (upper_long - lower_long) / (df.shape[1] - 1)

    closest_lat_idx = int((upper_lat - gs_lat) / lat_step)
    closest_long_idx = int((upper_long - gs_long) / long_step)

    lat_idx_decimal = ((upper_lat - gs_lat) / lat_step) - closest_lat_idx
    long_idx_decimal = ((upper_long - gs_long) / long_step) - closest_long_idx

    # Ensure indices are within bounds
    closest_lat_idx = max(0, min(closest_lat_idx, df.shape[0] - 2))
    closest_long_idx = max(0, min(closest_long_idx, df.shape[1] - 2))

    # Get the values of the four surrounding points
    top_left_value = df.iloc[closest_lat_idx, closest_long_idx]
    top_right_value = df.iloc[closest_lat_idx, closest_long_idx + 1]
    bottom_left_value = df.iloc[closest_lat_idx + 1, closest_long_idx]
    bottom_right_value = df.iloc[closest_lat_idx + 1, closest_long_idx + 1]

    # Perform bilinear interpolation
    interpolated_value = (
        top_left_value * (1 - lat_idx_decimal) * (1 - long_idx_decimal)
        + top_right_value * (1 - lat_idx_decimal) * long_idx_decimal
        + bottom_left_value * lat_idx_decimal * (1 - long_idx_decimal)
        + bottom_right_value * lat_idx_decimal * long_idx_decimal
    )

    # print(f"Interpolated GS height: {interpolated_value}")
    return interpolated_value
