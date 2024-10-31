def calculate_offset(point, elevation_df, shape):
    for i in range(shape[0]):
        for j in range(shape[1]):
            elevation_df[i, j, 0] = point[0] - float(elevation_df[i, j, 0])
            elevation_df[i, j, 1] = point[1] - float(elevation_df[i, j, 1])
            elevation_df[i, j, 2] = point[2] - float(elevation_df[i, j, 2])