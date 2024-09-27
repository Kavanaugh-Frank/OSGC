"""
Takes in the ceiling of the 4 coordinates that describe the requested window based on user
input, and calculates the number of base ( 1x1 Squares) tiff files it would take
to make the new image

Returns 1,2,4, or Error
"""

def calculate_num_files(upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil):
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