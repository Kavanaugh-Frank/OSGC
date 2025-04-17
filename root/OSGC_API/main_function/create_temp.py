import os
import uuid
import rasterio
from osgeo import gdal
from flask import abort

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
        HTTPException: If the temporary file cannot be opened, an HTTP 500 error is raised.
    """
    temp_file_name = f"{uuid.uuid4()}.tiff"
    full_temp_file_name = os.path.join(holder_directory, temp_file_name)

    # creating the blank tiff that will be overwritten
    driver = gdal.GetDriverByName("GTiff")
    # 1 is the Height, Width, and Number of Channels of this blank file
    try:
        driver.Create(full_temp_file_name, 1, 1, 1, gdal.GDT_Byte)
    except:
        abort(404, "Creation of Blank TIFF failed")

    try:
        with rasterio.open(full_temp_file_name) as img:
            pass
            # print("Temporary file created successfully.")
    except Exception as e:
        abort(500, f"Failed to open temp file: {e}")

    return full_temp_file_name
