def get_gs_height(upper_lat, upper_long, lower_lat, lower_long, df, gs_lat, gs_long):
    lat_step = (upper_lat - lower_lat) / df.shape[0]
    long_step = (upper_long - lower_long) / df.shape[1]

    closest_lat_idx = round((upper_lat - gs_lat) / lat_step)
    closest_long_idx = round((upper_long - gs_long) / long_step)

    surrounding_points = [
        (closest_lat_idx, closest_long_idx),
        (closest_lat_idx - 1, closest_long_idx),
        (closest_lat_idx + 1, closest_long_idx),
        (closest_lat_idx, closest_long_idx - 1),
        (closest_lat_idx, closest_long_idx + 1),
    ]

    valid_points = [
        df.iloc[lat_idx, long_idx] for lat_idx, long_idx in surrounding_points
    ]
    gs_point = sum(valid_points) / len(valid_points)
    print(f"Average GS height from surrounding points: {gs_point}")
    # print("Steps", lat_step, long_step)
    return gs_point