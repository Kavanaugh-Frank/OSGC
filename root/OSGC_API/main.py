import math
import os
import logging

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

# Makes the 3 vectors needed for the translation matrix, and puts each point through that basis
from main_function.translation_basis import translation_basis

# Finds the height at the point that represents the GS in the DF before it is shrunken
from main_function.gs_height import get_gs_height

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Suppress logs from external libraries
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger("osgeo").setLevel(logging.ERROR)

app = Flask(__name__)


@app.route("/process_coordinates", methods=["POST"])
def process_coordinates():
    logging.info("Received a request to /process_coordinates")
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
        gs_height = float(data.get("gs_height"))  # meter
        offset = float(data.get("offset"))  # meter
        heading = float(data.get("heading")) # heading of the airport in degrees (clockwise from true North)

        logging.info(f"Request parameters: {data}")
    except (TypeError, ValueError) as e:
        logging.error(f"Invalid input data: {e}")
        abort(400, f"Invalid input data: {e}")

    if num_x_slice <= 0 and num_y_slice <= 0:
        logging.error("num_x_slice and num_y_slice must be positive integers")
        abort(400, "num_x_slice and num_y_slice must be positive integers")

    if not -90 <= upper_lat <= 90 and -90 <= lower_lat <= 90:
        logging.error("Latitude values must be between -90 and 90 degrees")
        abort(400, "Latitude values must be between -90 and 90 degrees")

    if not -180 <= upper_long <= 180 and -180 <= lower_long <= 180:
        logging.error("Longitude values must be between -180 and 180 degrees")
        abort(400, "Longitude values must be between -180 and 180 degrees")

    if not abs(upper_lat) >= abs(lower_lat):
        logging.error("upper_lat must be greater than or equal to lower_lat")
        abort(400, "upper_lat must be greater than or equal to lower_lat")

    if not abs(upper_long) >= abs(lower_long):
        logging.error("upper_long must be greater than or equal to lower_long")
        abort(400, "upper_long must be greater than or equal to lower_long")

    if gs_height < 0:
        logging.error("gs_height must be a non-negative value")
        abort(400, "gs_height must be a non-negative value")

    if heading < 0:
        logging.error("heading must be a value greater than 0")
        abort(400, "heading must be a value greater than 0")

    # keep it between 0-360 without throwing an error
    if heading > 360:
        logging.info("heading was above 360 and had 360 subtracted to it")
        heading = heading - 360

    upper_lat_ceil = math.ceil(abs(upper_lat))
    lower_lat_ceil = math.ceil(abs(lower_lat))
    upper_long_ceil = math.ceil(abs(upper_long))
    lower_long_ceil = math.ceil(abs(lower_long))

    logging.info(f"Looking up file based on coordinates: upper_lat={upper_lat}, upper_long={upper_long}, lower_lat={lower_lat}, lower_long={lower_long}")
    file = look_up_file(
        upper_lat_ceil,
        upper_long_ceil,
        upper_lat,
        upper_long,
        base_dir=volume_directory,
    )

    if file is None:
        logging.error("File not found")
        abort(404, "File not found")

    full_temp_file_name = create_temp_file()
    full_merged_file_name = create_temp_file()

    lat_diff = abs(upper_lat_ceil - lower_lat_ceil)
    long_diff = abs(upper_long_ceil - lower_long_ceil)

    num_files_needed = 0

    if (lat_diff == 1 and long_diff == 0) or (lat_diff == 0 and long_diff == 1):
        num_files_needed = 2
    elif lat_diff == 1 and long_diff == 1:
        num_files_needed = 4
    elif lat_diff == 0 and long_diff == 0:
        num_files_needed = 1
    else:
        logging.error("Invalid latitude or longitude difference for file calculation")
        abort(404, "Invalid latitude or longitude difference for file calculation")

    logging.info(f"Processing {num_files_needed} files")
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

    count_invalid = (df == -999999.0).sum().sum()
    logging.info(f"Number of -999999 values before replacement: {count_invalid}")
    df.replace(-999999.0, None, inplace=True)
    df.fillna("ffill", inplace=True)

    df = df.astype(float)
    max_value = df.max().max()
    min_value = df.min().min()
    logging.info(f"Highest value in the DataFrame: {max_value}")
    logging.info(f"Lowest value in the DataFrame: {min_value}")
    logging.info(f"Data Frame Shape before Interpolation: {df.shape}")

    try:
        gs_point = get_gs_height(upper_lat, upper_long, lower_lat, lower_long, df, gs_lat, gs_long)
        logging.info(f"Height of the elevation where the GS is located {gs_point}")
    except Exception as e:
        logging.error(f"Problem finding the GS height: {e}")
        abort(404, f"Problem {e} finding the GS height")

    gs_height = gs_height + gs_point

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
        logging.info(f"Data Frame Shape after Interpolation: {shrunk_data.shape}")
    except Exception as e:
        logging.error(f"Interpolation failed: {e}")
        abort(404, f"Interpolation failed with error: {e}")

    try:
        shrunk_json = translation_basis(shrunk_data, offset, gs_lat, gs_long, gs_height, heading)
    except Exception as e:
        logging.error(f"Translation basis failed: {e}")
        abort(404, f"Translation basis failed: {e}")

    for temp_file in [full_temp_file_name, full_merged_file_name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            logging.warning(f"{temp_file} not found. Skipping removal.")
        except PermissionError:
            logging.warning(f"Permission denied when trying to remove {temp_file}. Skipping removal.")
        except Exception as e:
            logging.error(f"Error removing {temp_file}: {e}")

    flattened_data = shrunk_json.values.flatten().tolist()

    with open("elevation.3D", "w", encoding="utf-8") as f:
        f.write(f"  {num_y_slice}           {num_x_slice}\n")
        for row in flattened_data:
            f.write(f" {row[0]} {row[1]} {row[2]}\n")

    logging.info("Request processed successfully")
    return jsonify(flattened_data)


app.run(host="0.0.0.0", port=8080, debug=True)
