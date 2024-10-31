"""
Finds a returns the resolution (height and width in pixels) of the requested tiff file
"""
import rasterio

def get_resolution(tiff_path):
    with rasterio.open(tiff_path) as src:
        resolution_width = src.width
        resolution_height = src.height
    return resolution_width, resolution_height