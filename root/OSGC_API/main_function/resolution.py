import rasterio

def get_resolution(tiff_path):
    """
    Get the resolution (width and height) of a TIFF image.

    Parameters:
    tiff_path (str): The file path to the TIFF image.

    Returns:
    tuple: A tuple containing the width and height of the TIFF image.
    """
    with rasterio.open(tiff_path) as src:
        resolution_width = src.width
        resolution_height = src.height
    return resolution_width, resolution_height