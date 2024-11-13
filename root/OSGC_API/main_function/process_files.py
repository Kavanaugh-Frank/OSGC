import rasterio
from flask import abort
from osgeo import gdal
import pandas as pd
import math

from helpers.calculate_shape import calculate_shape
from main_function.lookup_file import look_up_file
from config import volume_directory

"""
This python file provides functions to process geospatial files based on specified coordinates, resolution, and the number
of input files required. Depending on the area of interest, it processes one, two, or four TIFF files to extract
a specific window of pixel values and convert it into a DataFrame format. The main function, `process_files`,
directs the processing workflow based on the number of files needed.

Functions:
    - process_files: Determines how many files need to be processed (1, 2, or 4) and calls the appropriate function.
    - process_single_file: Processes a single file by extracting a window based on given coordinates and resolution.
    - process_two_files: Processes two files by merging them and extracting a specified window from the merged file.
    - process_four_files: Processes four files by creating a mosaic and extracting a specified window from it.

Parameters:
    - num_files_needed (int): The number of files required for processing. Expected values are 1, 2, or 4.
    - file (str): The path to the main input file.
    - upper_lat (float): The upper latitude boundary for the area of interest.
    - upper_long (float): The upper longitude boundary for the area of interest.
    - lower_lat (float): The lower latitude boundary for the area of interest.
    - lower_long (float): The lower longitude boundary for the area of interest.
    - resolution_width (int): The desired resolution width of the output data.
    - full_temp_file_name (str): Path to the temporary file for storing extracted windows.
    - full_merged_file_name (str): Path to the merged file for storing combined data if multiple files are processed.

Returns:
    - pd.DataFrame: A DataFrame containing the extracted pixel data for the specified area of interest.

Exceptions:
    - Raises an HTTP 404 error if:
        - The number of files needed is not 1, 2, or 4.
        - Required files for merging cannot be found.

Usage:
    This module is primarily used to extract specific geospatial data from one or more TIFF files based on a defined
    latitude and longitude range. The extracted data is returned as a pandas DataFrame, making it suitable for further
    analysis or visualization in geospatial data processing pipelines.
"""

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
    str: The path to the processed file.

    Raises:
    HTTPException: If the number of files needed is not 1, 2, or 4, a 404 error is raised with a message indicating the issue.
    """
    if num_files_needed == 1:
        return process_single_file(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name)
    elif num_files_needed == 2:
        return process_two_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name)
    elif num_files_needed == 4:
        return process_four_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name)
    else:
        abort(404, "The Input Coordinates could not resolve in 1, 2, or 4 TIFF files")


def process_single_file(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name):
    """
    Processes a single file by extracting a specified window and converting it to a DataFrame.

    Args:
        file (str): The path to the input file.
        upper_lat (float): The upper latitude of the window.
        upper_long (float): The upper longitude of the window.
        lower_lat (float): The lower latitude of the window.
        lower_long (float): The lower longitude of the window.
        resolution_width (int): The resolution width for the window.
        full_temp_file_name (str): The path to the temporary file to store the extracted window.

    Returns:
        pd.DataFrame: A DataFrame containing the pixel values of the extracted window.
    """
    window = calculate_shape(upper_lat, upper_long, lower_lat, lower_long, resolution_width)
    gdal.Translate(full_temp_file_name, file, srcWin=window)
    img = rasterio.open(full_temp_file_name)
    full_img = img.read()
    df = pd.DataFrame(full_img[0])
    img.close()
    return df


def process_two_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name):
    """
    Processes two geospatial files by merging them and extracting a specific window of data.

    Args:
        file (str): The path to the first file to be processed.
        upper_lat (float): The upper latitude boundary for the area of interest.
        upper_long (float): The upper longitude boundary for the area of interest.
        lower_lat (float): The lower latitude boundary for the area of interest.
        lower_long (float): The lower longitude boundary for the area of interest.
        resolution_width (int): The resolution width for the output data.
        full_temp_file_name (str): The path to the temporary file where the extracted window will be saved.
        full_merged_file_name (str): The path to the file where the merged data will be saved.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the extracted window.

    Raises:
        HTTPException: If the lower file is not found, an HTTP 404 error is raised.
    """
    lower_file = look_up_file(math.ceil(lower_lat), math.ceil(lower_long), lower_lat, lower_long, base_dir=volume_directory)
    if lower_file is None:
        abort(404, "Lower file not found")

    files_to_merge = [file, lower_file]
    g = gdal.Warp(full_merged_file_name, files_to_merge, format="GTiff")
    g = None

    window = calculate_shape(upper_lat, upper_long, lower_lat, lower_long, resolution_width)
    gdal.Translate(full_temp_file_name, full_merged_file_name, srcWin=window)

    img = rasterio.open(full_temp_file_name)
    full_img = img.read()
    df = pd.DataFrame(full_img[0])
    img.close()
    return df


def process_four_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name):
    """
    Processes four files to create a mosaic and extracts a specific window from the mosaic.

    Args:
        file (str): The path to the initial file to be included in the mosaic.
        upper_lat (float): The upper latitude boundary for the area of interest.
        upper_long (float): The upper longitude boundary for the area of interest.
        lower_lat (float): The lower latitude boundary for the area of interest.
        lower_long (float): The lower longitude boundary for the area of interest.
        resolution_width (int): The resolution width for the output image.
        full_temp_file_name (str): The path to the temporary file where the extracted window will be saved.
        full_merged_file_name (str): The path to the file where the merged mosaic will be saved.

    Returns:
        pd.DataFrame: A DataFrame containing the pixel values of the extracted window from the mosaic.

    Raises:
        HTTPException: If one of the mosaic files is not found.
    """
    bottom_left_file = look_up_file(math.ceil(upper_lat), math.ceil(lower_long), upper_lat, lower_long, base_dir=volume_directory)
    bottom_right_file = look_up_file(math.ceil(lower_lat), math.ceil(lower_long), lower_lat, lower_long, base_dir=volume_directory)
    top_right_file = look_up_file(math.ceil(lower_lat), math.ceil(upper_long), lower_lat, lower_long, base_dir=volume_directory)

    if None in [bottom_left_file, bottom_right_file, top_right_file]:
        abort(404, "One of the mosaic files was not found")

    files_to_merge = [file, bottom_right_file, top_right_file, bottom_left_file]
    g = gdal.Warp(full_merged_file_name, files_to_merge, format="GTiff")
    g = None

    window = calculate_shape(upper_lat, upper_long, lower_lat, lower_long, resolution_width)
    gdal.Translate(full_temp_file_name, full_merged_file_name, srcWin=window)

    img = rasterio.open(full_temp_file_name)
    full_img = img.read()
    df = pd.DataFrame(full_img[0])
    img.close()
    return df