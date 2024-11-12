from functions.shrink_array import interpolation
from helpers.calculate_offset import calculate_offset
from flask import abort
import pandas as pd

def shrink_and_convert_to_json(df, num_x_slice, num_y_slice, upper_lat, upper_long, lower_lat, lower_long, point):
    try:
        shrunk_data = interpolation(df, num_x_slice, num_y_slice, upper_lat, upper_long, abs(upper_lat - lower_lat), abs(upper_long - lower_long))
        shape = shrunk_data.shape
        shrunk_json = shrunk_data.to_json(orient="values")
    except Exception as e:
        abort(404, f"Shrinking Failed {e}")
        
    return shrunk_json, shape