# import rasterio
from flask import Flask, request, jsonify, abort
from osgeo import gdal


from helpers.calculate_files import calculate_num_files  # Calculates the number of files needed based on coordinates
from helpers.lookup_file import look_up_file  # Looks up the file based on given coordinates
from helpers.resolution import get_resolution  # Retrieves the resolution of a given file
from helpers.cleanup import cleanup_temp_files  # Cleans up temporary files created during processing
from helpers.shrink_convert import shrink_and_convert_to_json  # Shrinks data and converts it to JSON format
from helpers.process_files import process_files  # Processes the files based on given parameters
from helpers.create_temp import create_temp_file  # Creates a temporary file for intermediate processing
from helpers.get_data import extract_request_data, calculate_ceilings  # Extracts data from the request and calculates ceiling values for coordinates

from config import volume_directory

gdal.DontUseExceptions()

app = Flask(__name__)


@app.route("/process_coordinates", methods=["POST"])
def process_coordinates():
    data = request.json
    num_x_slice, num_y_slice, upper_lat, lower_lat, upper_long, lower_long, radar_lat, radar_long = (
        extract_request_data(data)
    )
    upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil = (
        calculate_ceilings(upper_lat, lower_lat, upper_long, lower_long)
    )

    file = look_up_file(
        upper_lat_ceil,
        upper_long_ceil,
        upper_lat,
        upper_long,
        base_dir=volume_directory,
    )
    if file is None:
        abort(404, "File not found")

    resolution_width, resolution_height = get_resolution(file)
    if resolution_width != resolution_height:
        print("The height and width does not match")

    temp_file_name, full_temp_file_name = create_temp_file()
    merged_file_name, full_merged_file_name = create_temp_file()

    num_files_needed = calculate_num_files(
        upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil
    )
    df = process_files(
        num_files_needed,
        file,
        upper_lat,
        upper_long,
        lower_lat,
        lower_long,
        resolution_width,
        full_temp_file_name,
        full_merged_file_name,
    )

    # the [0,0,0] is the offset point, this should be user input at some point
    shrunk_json, shape = shrink_and_convert_to_json(
        df, num_x_slice, num_y_slice, upper_lat, upper_long, lower_lat, lower_long, [radar_lat,radar_long,0]
    )

    cleanup_temp_files([full_temp_file_name, full_merged_file_name])

    return jsonify({"shape": shape, "data": shrunk_json})


app.run(host="0.0.0.0", port=8080, debug=True)
