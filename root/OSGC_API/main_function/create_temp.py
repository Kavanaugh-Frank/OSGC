import os
import uuid
import rasterio
from flask import abort

from helpers.tiff_func import create_blank_tiff
from config import holder_directory

def create_temp_file():
    """
    Creates a temporary TIFF file with a unique name in the specified directory.

    This function generates a unique filename using UUID, creates a blank TIFF file
    with that name in the specified directory, and attempts to open it using rasterio
    to ensure it was created successfully.

    Returns:
        tuple: A tuple containing the temporary file name and the full path to the temporary file.

    Raises:
        HTTPException: If the temporary file cannot be opened, an HTTP 500 error is raised with the error message.
    """
    temp_file_name = f"{uuid.uuid4()}.tiff"
    full_temp_file_name = os.path.join(holder_directory, temp_file_name)
    create_blank_tiff(full_temp_file_name)
    try:
        with rasterio.open(full_temp_file_name) as img:
            print("Temporary file created successfully.")
    except Exception as e:
        abort(500, f"Failed to open temp file: {e}")
    return temp_file_name, full_temp_file_name