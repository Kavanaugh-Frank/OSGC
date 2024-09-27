import math


"""
Takes in the 4 coordinate points that describe the requested area
by the user, and calculates the resolution of the new window
based on the resolution of the base images.

Returns tuple with the new window information

"""
def calculate_shape(upper_lat, upper_long, lower_lat, lower_long,  resolution):
    upper_lat = abs(upper_lat)
    upper_long = abs(upper_long)
    lower_lat = abs(lower_lat)
    lower_long = abs(lower_long)

    # either resolution should work as long as they are even
    start_lat = int(math.floor(upper_lat % 1 * resolution))
    start_long = int(math.floor(upper_long % 1 * resolution))
    new_height = int(abs((upper_lat - lower_lat) * resolution))
    new_width = int(abs((upper_long - lower_long) * resolution))

    # SrcWin requires (start_x, start_y, width, height)
    window = (start_lat, start_long, new_width, new_height)
    print("New Window Shape ", window)
    return window