def calculate_num_files(upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil):
    """
    Takes in the ceiling of the 4 coordinates that describe the requested window based on user
    input, and calculates the number of base ( 1x1 Squares) tiff files it would take
    to make the new image.

    Parameters:
    upper_lat_ceil (int): The upper latitude boundary.
    lower_lat_ceil (int): The lower latitude boundary.
    upper_long_ceil (int): The upper longitude boundary.
    lower_long_ceil (int): The lower longitude boundary.

    Returns:
    int: The number of files calculated based on the boundaries.
         Returns 1 if the upper and lower boundaries for both latitude and longitude are the same.
         Returns 2 if the upper and lower boundaries for either latitude or longitude differ by 1.
         Returns 4 if the upper and lower boundaries for both latitude and longitude differ by 1.
         Returns "Error" if the boundaries do not match any of the above conditions.
    """
    if upper_lat_ceil == lower_lat_ceil and upper_long_ceil == lower_long_ceil:
        return 1
    elif any([
        (upper_lat_ceil == lower_lat_ceil and upper_long_ceil == lower_long_ceil + 1),
        (upper_lat_ceil == lower_lat_ceil + 1 and upper_long_ceil == lower_long_ceil)
    ]):
        return 2
    elif (upper_lat_ceil == lower_lat_ceil + 1) and (upper_long_ceil == lower_long_ceil + 1):
        return 4 
    else:
        return "Error"