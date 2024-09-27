import math

# this is the new shape calculation that needs to be tested
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
    # print("New Window Shape ", window)
    return window

def test_calculate_shape():
    assert calculate_shape(30, -90, 29, -89, 10812) == (0, 0, 10812, 10812)
    assert calculate_shape(29.5, -89.5, 29, -89, 10812) == (5406, 5406, 5406, 5406)
    assert calculate_shape(29.5, -89.5, 29.4, -89.4, 10812) == (5406, 5406, 1081, 1081)
    
    assert calculate_shape(30, -90, 29, -89, 0) == (0, 0, 0, 0)
    
    assert calculate_shape(-30, -90, -31, -89, 10812) == (0, 0, 10812, 10812)
    assert calculate_shape(-29.5, -89.5, -29, -89, 10812) == (5406, 5406, 5406, 5406)
    
    assert calculate_shape(30, -90, 29, -89, 1000000) == (0, 0, 1000000, 1000000)
    
    assert calculate_shape(30, -90, 30, -90, 10812) == (0, 0, 0, 0)
    
    assert calculate_shape(29, -89, 30, -90, 10812) == (0, 0, 10812, 10812)
    
    assert calculate_shape(30, -90, 29, -89, 1234.567) == (0, 0, 1234, 1234)
    
    assert calculate_shape(0, -90, -1, -89, 10812) == (0, 0, 10812, 10812)

