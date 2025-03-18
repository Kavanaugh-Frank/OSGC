from osgeo import gdal
from flask import abort

def df_to_tiff(df, output_tiff_path):
    """
    Converts a pandas DataFrame to a TIFF file.
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to be converted to TIFF.
    output_tiff_path (str): The file path where the output TIFF file will be saved.
    Returns:
    None
    """

    print("Converting DataFrame to TIFF...")
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