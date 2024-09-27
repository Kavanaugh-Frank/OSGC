import os
import math
import uuid
import rasterio
import pandas as pd
import georasters as gr
from flask import Flask, request, jsonify, abort, send_file, Response
from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib
import threading
import math
import numpy as np

from functions.shrink_array import shrink_dataframe
from functions.calculate_files import calculate_num_files
from functions.lookup_file import look_up_file
from functions.tiff_func import create_blank_tiff
from functions.tiff_func import df_to_tiff
from functions.tiff_func import get_resolution
from functions.calculate_shape import calculate_shape


matplotlib.use('Agg')
gdal.DontUseExceptions()

app = Flask(__name__)

# Path to the shared volume directory (mounted in the Docker container)
volume_directory = "/data"

@app.route('/process_coordinates', methods=['POST'])
def process_coordinates():
    # Get the JSON data from the POST request
    data = request.json

    # Get the untouched data
    upper_lat = float(data.get('upper_lat'))
    lower_lat = float(data.get('lower_lat'))
    upper_long = float(data.get('upper_long'))
    lower_long = float(data.get('lower_long'))
    print(upper_lat, upper_long, lower_lat, lower_long)

    # Ceiling
    upper_lat_ceil = math.ceil(abs(upper_lat))
    lower_lat_ceil = math.ceil(abs(lower_lat))
    upper_long_ceil = math.ceil(abs(upper_long))
    lower_long_ceil = math.ceil(abs(lower_long))
    print(upper_lat_ceil, upper_long_ceil, lower_lat_ceil, lower_long_ceil)

    # Look up the file in the shared volume directory
    file = look_up_file(upper_lat_ceil, upper_long_ceil, upper_lat, upper_long, base_dir=volume_directory)

    if file is None:
        abort(404, "File not found")
        
    resolution_width, resolution_height = get_resolution(file)
    if resolution_width != resolution_height:
        print("The height and width does not match")

    print("Width and Height of the Upper Left Lat and Long Image Only: ", resolution_width, resolution_height)

    # Define paths for the temp files
    temp_file_name = str(uuid.uuid4()) + '.tiff'
    full_temp_file_name = os.path.join(volume_directory, temp_file_name)

    merged_file_name = str(uuid.uuid4()) + '.tiff'
    full_merged_file_name = os.path.join(volume_directory, merged_file_name)

    # Create a blank TIFF file in the shared volume
    create_blank_tiff(full_temp_file_name)

    df = None
    num_files_needed = calculate_num_files(upper_lat_ceil, lower_lat_ceil, upper_long_ceil, lower_long_ceil)
    
    if num_files_needed == 1:
        window = calculate_shape(upper_lat, upper_long, lower_lat, lower_long, resolution_width)
        gdal.Translate(full_temp_file_name, file, srcWin=window)

        img = rasterio.open(full_temp_file_name)
        full_img = img.read()
        df = pd.DataFrame(full_img[0])
        img.close()
        
    elif num_files_needed == 2:
        lower_file = look_up_file(lower_lat_ceil, lower_long_ceil, lower_lat, lower_long, base_dir=volume_directory)
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

    elif num_files_needed == 4:
        bottom_left_file = look_up_file(upper_lat_ceil, lower_long_ceil, upper_lat, lower_long, base_dir=volume_directory)
        bottom_right_file = look_up_file(lower_lat_ceil, lower_long_ceil, lower_lat, lower_long, base_dir=volume_directory)
        top_right_file = look_up_file(lower_lat_ceil, upper_long_ceil, lower_lat, lower_long, base_dir=volume_directory)

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

    else:
        abort(404, "The Input Coordinates could not resolve in 1, 2, or 4 TIFF files")

    try:
        # Save the result to the shared volume
        # thread = threading.Thread(target=df_to_tiff(df, os.path.join(volume_directory, f"confirm.tiff")))
        # thread.start()

        # json_data = df.to_json(orient='values')
        
        try:
            shrunk_data = shrink_dataframe(df, 30)

            shape = shrunk_data.shape

            shrunk_json = shrunk_data.to_json(orient='values')

            return jsonify({
                'shape': shape,
                'data': shrunk_json
            })
            # return jsonify(shrunk_json)
        except:
            abort(404, "Shrinking Failed")
    

        return shrunk_data
        # return jsonify(json_data)

    finally:
        # Cleanup
        if os.path.exists(full_temp_file_name):
            os.remove(full_temp_file_name)
        if os.path.exists(full_merged_file_name):
            os.remove(full_merged_file_name)


app.run(host='0.0.0.0', port=8080, debug=True)