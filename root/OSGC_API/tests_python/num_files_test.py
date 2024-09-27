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
    
def test_single_file():
    # Test the case where only one file is needed
    assert calculate_num_files(2, 2, 3, 3) == 1
    assert calculate_num_files(0, 0, 1, 1) == 1
    assert calculate_num_files(-1, -1, 0, 0) == 1

def test_two_files():
    # Test the cases where two files are needed
    assert calculate_num_files(1, 1, 2, 1) == 2
    assert calculate_num_files(2, 1, 2, 2) == 2

def test_four_files():
    # Test the case where four files are needed
    assert calculate_num_files(2, 1, 3, 2) == 4
    assert calculate_num_files(0, -1, 1, 0) == 4
    assert calculate_num_files(-1, -2, 0, -1) == 4
    assert calculate_num_files(5, 4, 6, 5) == 4

def test_error():
    assert calculate_num_files(1,2,1,1) == "Error"
    assert calculate_num_files(1,1,1,2) == "Error"
    assert calculate_num_files(1,3,1,1) == "Error"
    assert calculate_num_files(1,2,1,3) == "Error"