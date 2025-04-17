import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource (for PyInstaller compatibility) """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller stores temp path here
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def look_up_file(x, y, x_sign, y_sign, base_dir="data"):
    """
    Constructs a file name based on coordinates and checks if it exists.
    Compatible with PyInstaller.
    """
    x_position = "n" if x_sign > 0 else "s"
    y_position = "e" if y_sign > 0 else "w"

    # Format filename with leading zero if y < 100
    if y >= 100:
        file_name = f"{x_position}{abs(x)}{y_position}{abs(y)}.tiff"
    else:
        file_name = f"{x_position}{abs(x)}{y_position}0{abs(y)}.tiff"

    print("File Name:", file_name)
    base_dir = "data"
    # Resolve the path using resource_path
    full_path = resource_path(os.path.join(base_dir, file_name))

    print("File Full Path:", full_path)

    if os.path.isfile(full_path):
        print(file_name, "is a file")
        return full_path

    return None
