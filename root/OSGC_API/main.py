# import rasterio
from flask import Flask, request, jsonify, abort
from osgeo import gdal


from main_function.calculate_files import calculate_num_files  # Calculates the number of files needed based on coordinates
from main_function.lookup_file import look_up_file  # Looks up the file based on given coordinates
from main_function.resolution import get_resolution  # Retrieves the resolution of a given file
from main_function.cleanup_temp import cleanup_temp_files  # Cleans up temporary files created during processing
from main_function.shrink import shrink  # Shrinks data and converts it to JSON format
from main_function.process_files import process_files  # Processes the files based on given parameters
from main_function.create_temp import create_temp_file  # Creates a temporary file for intermediate processing
from main_function.get_data import extract_request_data  # Extracts data from the request and calculates ceiling values for coordinates
from main_function.translation_basis import translation_basis  # makes the 3 vectors needed for the translation matrix
from helpers.tiff_func import df_to_tiff  # Converts a dataframe to a tiff file

from config import volume_directory
import math

gdal.DontUseExceptions()

app = Flask(__name__)


@app.route("/process_coordinates", methods=["POST"])
def process_coordinates():
    data = request.json
    num_x_slice, num_y_slice, upper_lat, lower_lat, upper_long, lower_long, gs_lat, gs_long, gs_height, offset = (
        extract_request_data(data)
    )

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

    # output_path = "/app/temp.tiff"
    # df_to_tiff(df, output_path)
    
    shrunk_data, shape = shrink(
        df, num_x_slice, num_y_slice, upper_lat, upper_long, lower_lat, lower_long, [gs_lat,gs_long,gs_height]
    )

    shrunk_json = translation_basis(shrunk_data, offset, gs_lat, gs_long, gs_height)

    cleanup_temp_files([full_temp_file_name, full_merged_file_name])

    return shrunk_json.to_json(orient="values")


app.run(host="0.0.0.0", port=8080, debug=True)
