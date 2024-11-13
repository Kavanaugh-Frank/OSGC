import math

def calculate_shape(upper_lat, upper_long, lower_lat, lower_long,  resolution):
    """
    Calculate the shape of a window based on given latitude and longitude coordinates and resolution.
    Args:
        upper_lat (float): The upper latitude coordinate.
        upper_long (float): The upper longitude coordinate.
        lower_lat (float): The lower latitude coordinate.
        lower_long (float): The lower longitude coordinate.
        resolution (int): The resolution to be used for calculations.
    Returns:
        tuple: A tuple representing the window shape in the format (start_lat, start_long, new_width, new_height).
    """        
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
    # print("New Window Shape ", window)
    return window