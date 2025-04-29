import os
import sys
import requests
 
 
def resource_path(relative_path):
    """Get the absolute path to the resource (for PyInstaller compatibility)"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller stores temp path here
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
 
 
def look_up_file(x, y, x_sign, y_sign, base_dir="data"):
    """
    Constructs a file name based on coordinates and checks if it exists.
    Compatible with PyInstaller.
    """
    x_position = "n" if x_sign > 0 else "s"
    y_position = "e" if y_sign > 0 else "w"
 
    # Format filename with leading zero if y < 100
    if y >= 100:
        file_name = f"{x_position}{abs(x)}{y_position}{abs(y)}.tiff"
    else:
        file_name = f"{x_position}{abs(x)}{y_position}0{abs(y)}.tiff"
 
    print("File Name:", file_name)
    base_dir = "data"
    # Resolve the path using resource_path
    full_path = resource_path(os.path.join(base_dir, file_name))
 
    if not os.path.isfile(full_path):
        download_tiff(file_name, base_dir)
 
    print("File Full Path:", full_path)
 
    if os.path.isfile(full_path):
        print(file_name, "is a file")
        return full_path
 
    return None
 
 
def download_tiff(tiff, save_directory):
    # URL of the file to download
    url = f"https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/current/{tiff[:-5]}/USGS_13_{tiff[:-5]}.tif"
    print(url)
    # Send a GET request with stream=True to handle large files
    response = requests.get(url, stream=True)
    print(response.status_code)
    # Check if the request was successful
    if response.status_code == 200:
        # # Try to extract the filename from the Content-Disposition header
        # if "Content-Disposition" in response.headers:
        #     # Extract the filename from the header (if present)
        #     filename = (
        #         response.headers["Content-Disposition"]
        #         .split("filename=")[-1]
        #         .strip('"')
        #     )
        # else:
        #     # Otherwise, fallback to the default filename or URL's last segment
        #     filename = os.path.basename(url)
 
        print("Started Download")
        # tiff = tiff
        save_directory = resource_path(save_directory)
        filepath = os.path.join(save_directory, tiff)
        print(filepath)
 
        # Save the file with the extracted or fallback filename
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
 
        print(f"Download completed: {filepath}")
    else:
        print(f"Failed to download file: {tiff}")