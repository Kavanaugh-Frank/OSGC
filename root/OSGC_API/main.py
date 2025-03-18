# import rasterio
from flask import Flask, request, jsonify, abort
from osgeo import gdal
import os
import decimal
import rasterio

from main_function.lookup_file import look_up_file  # Looks up the file based on given coordinates
from main_function.process_files import process_files  # Processes the files based on given parameters
from main_function.create_temp import create_temp_file  # Creates a temporary file for intermediate processing
from main_function.shrink_array import interpolation
from main_function.translation_basis import translation_basis  # makes the 3 vectors needed for the translation matrix

from config import volume_directory
import math

gdal.DontUseExceptions()

app = Flask(__name__)


@app.route("/process_coordinates", methods=["POST"])
def process_coordinates():
    data = request.json

    num_x_slice = data.get("num_x_slice")
    num_y_slice = data.get("num_y_slice")
    upper_lat = float(data.get("upper_lat"))
    lower_lat = float(data.get("lower_lat"))
    upper_long = float(data.get("upper_long"))
    lower_long = float(data.get("lower_long"))
    gs_lat = float(data.get("gs_lat"))
    gs_long = float(data.get("gs_long"))
    gs_height = float(data.get("gs_height"))
    offset = float(data.get("offset"))

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

    # resolution_width, resolution_height = get_resolution(file)
    with rasterio.open(file) as src:
        resolution_width = src.width
        resolution_height = src.height
    
    if resolution_width != resolution_height:
        print("The height and width does not match")

    temp_file_name, full_temp_file_name = create_temp_file()
    merged_file_name, full_merged_file_name = create_temp_file()

    # calculating the number of files needed
    lat_diff = abs(upper_lat_ceil - lower_lat_ceil)
    long_diff = abs(upper_long_ceil - lower_long_ceil)

    if lat_diff == 0 and long_diff == 0:
        num_files_needed = 1
    elif (lat_diff == 1 and long_diff == 0) or (lat_diff == 0 and long_diff == 1):
        num_files_needed = 2
    elif lat_diff == 1 and long_diff == 1:
        num_files_needed = 4
    else:
        abort(404, "Unable to calculate the number of files required")

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

    # replacing the no_data value holder with 0 instead
    df.replace(-999999.0, 0, inplace=True)
    
    print("Data Frame Shape before Interpolation ", df.shape)
    # ds = gdal.Open(file)
    # print(f"Raster CRS: {ds.GetProjection()}")
    # print(f"Raster Extent (ULX, ULY, LRX, LRY): {ds.GetGeoTransform()}")
    
    try:
        shrunk_data = interpolation(df, num_x_slice, num_y_slice, upper_lat, upper_long, abs(upper_lat - lower_lat), abs(upper_long - lower_long), [gs_lat,gs_long,gs_height])
        shape = shrunk_data.shape
        # return shrunk_data.to_json(orient="values")
        print("Data Frame Shape after Interpolation ", shape)
    except Exception as e:
        abort(404, f"Shrinking Failed {e}")

    # putting the json to the basis of the glide-slope
    shrunk_json = translation_basis(shrunk_data, offset, gs_lat, gs_long, gs_height)
    
    # removing any of the temporary files that were created
    for temp_file in [full_temp_file_name, full_merged_file_name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            print(f"{temp_file} not found. Skipping removal.")
        except Exception as e:
            print(f"Error removing {temp_file}: {e}")


    return shrunk_json.to_json(orient="values")


app.run(host="0.0.0.0", port=8080, debug=True)
