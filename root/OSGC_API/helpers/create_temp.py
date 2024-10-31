import os
import uuid
import rasterio
from flask import abort

from functions.tiff_func import create_blank_tiff


from config import holder_directory

def create_temp_file():
    temp_file_name = f"{uuid.uuid4()}.tiff"
    full_temp_file_name = os.path.join(holder_directory, temp_file_name)
    create_blank_tiff(full_temp_file_name)
    try:
        with rasterio.open(full_temp_file_name) as img:
            print("Temporary file created successfully.")
    except Exception as e:
        abort(500, f"Failed to open temp file: {e}")
    return temp_file_name, full_temp_file_name