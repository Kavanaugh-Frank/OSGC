def extract_request_data(data):
    """
    Extracts and returns specific data from the post request.

    Args:
        data (dict): A dictionary containing the following keys:
            - "num_x_slice" (int): Number of slices along the x-axis.
            - "num_y_slice" (int): Number of slices along the y-axis.
            - "upper_lat" (str or float): Upper latitude boundary.
            - "lower_lat" (str or float): Lower latitude boundary.
            - "upper_long" (str or float): Upper longitude boundary.
            - "lower_long" (str or float): Lower longitude boundary.
            - "radar_lat" (str or float): Latitude of the radar.
            - "radar_long" (str or float): Longitude of the radar.
            - "radar_height" (str or float): Height of the radar.

    Returns:
        tuple: A tuple containing the following elements:
            - num_x_slice (int)
            - num_y_slice (int)
            - upper_lat (float)
            - lower_lat (float)
            - upper_long (float)
            - lower_long (float)
            - radar_lat (float)
            - radar_long (float)
            - radar_height (float)
    """
    num_x_slice = data.get("num_x_slice")
    num_y_slice = data.get("num_y_slice")
    upper_lat = float(data.get("upper_lat"))
    lower_lat = float(data.get("lower_lat"))
    upper_long = float(data.get("upper_long"))
    lower_long = float(data.get("lower_long"))
    radar_lat = float(data.get("radar_lat"))
    radar_long = float(data.get("radar_long"))
    radar_height = float(data.get("radar_height"))
    return num_x_slice, num_y_slice, upper_lat, lower_lat, upper_long, lower_long, radar_lat, radar_long, radar_height