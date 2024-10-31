from osgeo import gdal
from flask import abort

"""
Takes in the dataframe and the desired save location to take in the dataframe 
with elevation data and reacreates the TIFF file that the information comes from. 
Used mostly to double check the data in the dataframe matches the inputted TIFF

Does not return anything, but does save a TIFF file
"""
def df_to_tiff(df, output_tiff_path):
    # Extract data from the DataFrame
    array = df.values
    height, width = array.shape
    num_channels = 1  # Assuming it's a single-band image

    # Prepare the new TIFF file
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(output_tiff_path, width, height, num_channels, gdal.GDT_Float32)  # Adjust data type as needed

    # Write the pixel values to the new TIFF file
    for band_idx in range(num_channels):
        band = dataset.GetRasterBand(band_idx + 1)
        band.WriteArray(array)

    dataset = None  # Close the dataset

"""
Created a blank tiff file that is overwritten with the new elevation data
for the DF to Scatter plot function. Saves the output at a desired location
"""
def create_blank_tiff(output_tiff_path):
    # Create a blank TIFF file
    driver = gdal.GetDriverByName('GTiff')
    # 1 is the Height, Width, and Number of Channels of this blank file
    try:
        driver.Create(output_tiff_path, 1, 1, 1, gdal.GDT_Byte)
    except:
        abort(404, "Creation of Blank TIFF failed")