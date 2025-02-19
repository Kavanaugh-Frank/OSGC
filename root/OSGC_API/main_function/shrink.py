from flask import abort
from helpers.shrink_array import interpolation


def shrink(df, num_x_slice, num_y_slice, upper_lat, upper_long, lower_lat, lower_long, point):
    """
    Shrinks the given DataFrame using interpolation and converts the result to JSON format.

    Parameters:
    df (DataFrame): The input DataFrame to be shrunk.
    num_x_slice (int): The number of slices along the x-axis for interpolation.
    num_y_slice (int): The number of slices along the y-axis for interpolation.
    upper_lat (float): The upper latitude boundary for the interpolation.
    upper_long (float): The upper longitude boundary for the interpolation.
    lower_lat (float): The lower latitude boundary for the interpolation.
    lower_long (float): The lower longitude boundary for the interpolation.
    point (any): An additional parameter used in the interpolation function.

    Returns:
    tuple: A tuple containing the shrunk data in JSON format and the shape of the shrunk data.
    Raises:
    HTTPException: If the shrinking process fails, an HTTP 404 error is raised with the failure message.
    """
    try:
        shrunk_data = interpolation(df, num_x_slice, num_y_slice, upper_lat, upper_long, abs(upper_lat - lower_lat), abs(upper_long - lower_long), point)
        shape = shrunk_data.shape
    except Exception as e:
        abort(404, f"Shrinking Failed {e}")
        
    return shrunk_data, shape