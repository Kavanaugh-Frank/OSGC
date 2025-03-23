import csv
import math
import os

# Configuration for volume directory
from config import volume_directory

from flask import Flask, abort, jsonify, request

# Creates a temporary file for intermediate processing
from main_function.create_temp import create_temp_file

# Looks up the file based on given coordinates
from main_function.lookup_file import look_up_file

# Processes the files based on given parameters
from main_function.process_files import process_files

# Does the interpolation of the data into the smaller datasets
from main_function.shrink_array import interpolation

# Makes the 3 vectors needed for the translation matrix
from main_function.translation_basis import translation_basis
from osgeo import gdal

gdal.DontUseExceptions()

app = Flask(__name__)


@app.route("/process_coordinates", methods=["POST"])
def process_coordinates():
    """
    Processes geographical coordinates and performs various operations including validation, file lookup,
    data processing, interpolation, and translation.
    The function expects a JSON payload with the following keys:
    - num_x_slice: Number of slices along the x-axis (integer, positive)
    - num_y_slice: Number of slices along the y-axis (integer, positive)
    - upper_lat: Upper latitude boundary (float, between -90 and 90)
    - lower_lat: Lower latitude boundary (float, between -90 and 90)
    - upper_long: Upper longitude boundary (float, between -180 and 180)
    - lower_long: Lower longitude boundary (float, between -180 and 180)
    - gs_lat: Latitude of the glide slope (float)
    - gs_long: Longitude of the glide slope (float)
    - gs_height: Height of the glide slope (float, non-negative)
    - offset: Offset value for translation (float)
    The function performs the following steps:
    1. Validates the input data.
    2. Checks if the latitude and longitude values are within valid ranges.
    3. Ensures that the upper latitude/longitude is greater than or equal to the lower latitude/longitude.
    4. Looks up the required file based on the provided coordinates.
    5. Processes the files and performs interpolation.
    6. Translates the interpolated data based on the glide slope.
    7. Removes any temporary files created during processing.
    8. Converts the processed data into a flattened 1D array for JSON response.
    Returns:
        JSON response containing the flattened 1D array of processed data.
    Raises:
        400: If the input data is invalid or if any validation checks fail.
        404: If the required file is not found or if interpolation fails.
    """
    data = request.json

    try:
        num_x_slice = int(data.get("num_x_slice"))
        num_y_slice = int(data.get("num_y_slice"))
        upper_lat = float(data.get("upper_lat"))
        lower_lat = float(data.get("lower_lat"))
        upper_long = float(data.get("upper_long"))
        lower_long = float(data.get("lower_long"))
        gs_lat = float(data.get("gs_lat"))
        gs_long = float(data.get("gs_long"))
        gs_height = float(data.get("gs_height"))
        offset = float(data.get("offset"))
    except (TypeError, ValueError) as e:
        abort(400, f"Invalid input data: {e}")

    if num_x_slice <= 0 and num_y_slice <= 0:
        abort(400, "num_x_slice and num_y_slice must be positive integers")

    if not -90 <= upper_lat <= 90 and -90 <= lower_lat <= 90:
        abort(400, "Latitude values must be between -90 and 90 degrees")

    if not -180 <= upper_long <= 180 and -180 <= lower_long <= 180:
        abort(400, "Longitude values must be between -180 and 180 degrees")

    if not abs(upper_lat) >= abs(lower_lat):
        abort(400, "upper_lat must be greater than or equal to lower_lat")

    if not abs(upper_long) >= abs(lower_long):
        abort(400, "upper_long must be greater than or equal to lower_long")

    if gs_height < 0:
        abort(400, "gs_height must be a non-negative value")

    upper_lat_ceil = math.ceil(abs(upper_lat))
    lower_lat_ceil = math.ceil(abs(lower_lat))
    upper_long_ceil = math.ceil(abs(upper_long))
    lower_long_ceil = math.ceil(abs(lower_long))

    file = look_up_file(
        upper_lat_ceil,
        upper_long_ceil,
        upper_lat,
        upper_long,
        base_dir=volume_directory,
    )

    if file is None:
        abort(404, "File not found")

    full_temp_file_name = create_temp_file()
    full_merged_file_name = create_temp_file()

    # calculating the number of files needed
    lat_diff = abs(upper_lat_ceil - lower_lat_ceil)
    long_diff = abs(upper_long_ceil - lower_long_ceil)

    num_files_needed = 1

    if (lat_diff == 1 and long_diff == 0) or (lat_diff == 0 and long_diff == 1):
        num_files_needed = 2
    elif lat_diff == 1 and long_diff == 1:
        num_files_needed = 4
    else:
        abort(404, "Invalid latitude or longitude difference for file calculation")

    df = process_files(
        num_files_needed,
        file,
        upper_lat,
        upper_long,
        lower_lat,
        lower_long,
        full_temp_file_name,
        full_merged_file_name,
    )

    # preprocessing
    # this replaces the 'invalid" number with the last correct one in the row
    df.replace(-999999.0, method="ffill", inplace=True)

    print("Data Frame Shape before Interpolation ", df.shape)

    # ds = gdal.Open(file)
    # print(f"Raster CRS: {ds.GetProjection()}")
    # print(f"Raster Extent (ULX, ULY, LRX, LRY): {ds.GetGeoTransform()}")

    try:
        shrunk_data = interpolation(
            df,
            num_x_slice,
            num_y_slice,
            upper_lat,
            upper_long,
            abs(upper_lat - lower_lat),
            abs(upper_long - lower_long),
            [gs_lat, gs_long, gs_height],
        )
        shape = shrunk_data.shape
        print("Data Frame Shape after Interpolation ", shape)
    except Exception as e:
        abort(
            404,
            f"Interpolation failed with error: {e}. Parameters: "
            f"num_x_slice={num_x_slice}, num_y_slice={num_y_slice}, "
            f"upper_lat={upper_lat}, upper_long={upper_long}, "
            f"lower_lat={lower_lat}, lower_long={lower_long}, "
            f"gs_lat={gs_lat}, gs_long={gs_long}, gs_height={gs_height}",
        )
    try:
        shrunk_json = translation_basis(shrunk_data, offset, gs_lat, gs_long, gs_height)
    except Exception as e:
        abort(404, f"Translation basis failed: {e}")

    # removing any of the temporary files that were created
    for temp_file in [full_temp_file_name, full_merged_file_name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            print(f"{temp_file} not found. Skipping removal.")
        except PermissionError:
            print(
                f"Permission denied when trying to remove {temp_file}. Skipping removal."
            )
        except Exception as e:
            print(f"Error removing {temp_file}: {e}")

    # converting the 2D array to a single 1D array, while keeping the order
    # to match the format of the data table in OUGS
    flattened_data = shrunk_json.values.flatten().tolist()

    with open("elevation.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([upper_lat, upper_long, lower_lat, lower_long])
        for row in flattened_data:
            writer.writerow(row)

    return jsonify(flattened_data)


app.run(host="0.0.0.0", port=8080, debug=True)
