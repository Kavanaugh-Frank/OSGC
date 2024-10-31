import math

def extract_request_data(data):
    num_x_slice = data.get("num_x_slice")
    num_y_slice = data.get("num_y_slice")
    upper_lat = float(data.get("upper_lat"))
    lower_lat = float(data.get("lower_lat"))
    upper_long = float(data.get("upper_long"))
    lower_long = float(data.get("lower_long"))
    radar_lat = float(data.get("radar_lat"))
    radar_long = float(data.get("radar_long"))
    return num_x_slice, num_y_slice, upper_lat, lower_lat, upper_long, lower_long, radar_lat, radar_long


def calculate_ceilings(upper_lat, lower_lat, upper_long, lower_long):
    upper_lat_ceil = math.ceil(abs(upper_lat))
    lower_lat_ceil = math.ceil(abs(lower_lat))
    upper_long_ceil = math.ceil(abs(upper_long))
    lower_long_ceil = math.ceil(abs(lower_long))
    return upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil