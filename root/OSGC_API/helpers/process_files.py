import rasterio
from flask import abort
from osgeo import gdal
import pandas as pd
import math

from functions.calculate_shape import calculate_shape
from helpers.lookup_file import look_up_file

from config import volume_directory

def process_files(num_files_needed, file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name):
    if num_files_needed == 1:
        return process_single_file(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name)
    elif num_files_needed == 2:
        return process_two_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name)
    elif num_files_needed == 4:
        return process_four_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name)
    else:
        abort(404, "The Input Coordinates could not resolve in 1, 2, or 4 TIFF files")


def process_single_file(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name):
    window = calculate_shape(upper_lat, upper_long, lower_lat, lower_long, resolution_width)
    gdal.Translate(full_temp_file_name, file, srcWin=window)
    img = rasterio.open(full_temp_file_name)
    full_img = img.read()
    df = pd.DataFrame(full_img[0])
    img.close()
    return df


def process_two_files(file, upper_lat, upper_long, lower_lat, lower_long, resolution_width, full_temp_file_name, full_merged_file_name):
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