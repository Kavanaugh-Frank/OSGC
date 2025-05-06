import os
import sys

from main_function.lookup_file import resource_path
def setup_environment():
    # activate only when it is an executable
    if getattr(sys, 'frozen', False):
        # PROJ configuration
        os.environ['PROJ_LIB'] = resource_path('proj')
        os.environ['PROJ_DATA'] = resource_path('proj')
        # GDAL configuration
        os.environ['GDAL_DATA'] = resource_path('gdal')
        os.environ['GDAL_DRIVER_PATH'] = resource_path('gdal/plugins')

setup_environment()