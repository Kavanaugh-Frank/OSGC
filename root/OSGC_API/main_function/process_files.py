import rasterio
from flask import abort
from osgeo import gdal
import pandas as pd
import math

from main_function.lookup_file import look_up_file
from config import volume_directory

def process_files(num_files_needed, file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name):
    """
    Processes the given file(s) based on the number of files needed and the specified coordinates and resolution.

    Parameters:
    num_files_needed (int): The number of files needed for processing (1, 2, or 4).
    file (str): The path to the input file.
    upper_lat (float): The upper latitude coordinate.
    upper_long (float): The upper longitude coordinate.
    lower_lat (float): The lower latitude coordinate.
    lower_long (float): The lower longitude coordinate.
    resolution_width (int): The resolution width for processing.
    full_temp_file_name (str): The path to the temporary file to be used during processing.
    full_merged_file_name (str): The path to the merged file to be used if multiple files are processed.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted pixel data for the specified area of interest.

    Raises:
    HTTPException: If the number of files needed is not 1, 2, or 4, a 404 error is raised with a message indicating the issue.
    """
    files_to_merge = [file]

    if num_files_needed == 2:
        lower_file = look_up_file(math.ceil(lower_lat), math.ceil(lower_long), lower_lat, lower_long, base_dir=volume_directory)
        if lower_file is None:
            abort(404, "Lower file not found")
        files_to_merge.append(lower_file)
    elif num_files_needed == 4:
        bottom_left_file = look_up_file(math.ceil(upper_lat), math.ceil(lower_long), upper_lat, lower_long, base_dir=volume_directory)
        bottom_right_file = look_up_file(math.ceil(lower_lat), math.ceil(lower_long), lower_lat, lower_long, base_dir=volume_directory)
        top_right_file = look_up_file(math.ceil(lower_lat), math.ceil(upper_long), lower_lat, lower_long, base_dir=volume_directory)

        if None in [bottom_left_file, bottom_right_file, top_right_file]:
            abort(404, "One of the mosaic files was not found")

        files_to_merge.extend([bottom_left_file, bottom_right_file, top_right_file])
    elif num_files_needed != 1:
        abort(404, "The Input Coordinates could not resolve in 1, 2, or 4 TIFF files")

    if num_files_needed > 1:
        g = gdal.Warp(full_merged_file_name, files_to_merge, format="GTiff")
        g = None
        file_to_process = full_merged_file_name
    else:
        file_to_process = file

    translate_options = gdal.TranslateOptions(projWin=[upper_long, upper_lat, lower_long, lower_lat])
    gdal.Translate(full_temp_file_name, file_to_process, options=translate_options)

    img = rasterio.open(full_temp_file_name)
    full_img = img.read()
    df = pd.DataFrame(full_img[0])
    img.close()
    return df
