import os

"""
The function constructs a file name based on the latitude (`x`) and longitude (`y`) coordinates,
including appropriate formatting for northern/southern and eastern/western hemispheres.
It then checks if the file exists at the specified `base_dir`. 

If the file is found, the full path is returned; otherwise, None is returned.
"""

def look_up_file(x, y, x_sign, y_sign, base_dir="/data"):
    x_position = "n" if x_sign > 0 else "s"
    y_position = "e" if y_sign > 0 else "w"

    # Create the file name with appropriate formatting
    if y >= 100:
        file_name = f"{x_position}{abs(x)}{y_position}{abs(y)}.tiff"
    else:
        # y coordinates less than 100 need leading zero
        file_name = f"{x_position}{abs(x)}{y_position}0{abs(y)}.tiff"

    print("File Name: ", file_name)

    # Full path of the file to lookup in the shared volume
    full_path = os.path.join(base_dir, file_name)

    print("File Full Path: ", full_path)

    # Check if the file exists at the constructed path
    if os.path.isfile(full_path):
        print(file_name, "is a file")
        return full_path

    # If the file does not exist, return None
    return None