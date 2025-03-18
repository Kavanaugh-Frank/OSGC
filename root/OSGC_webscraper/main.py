import requests
import os

# List of TIFF files to download
# tiff_list = ["n42w085"]
tiff_list = ["n39w082", "n39w083", "n39w084", "n39w085",
             "n40w081", "n40w082", "n40w083", "n40w084", "n40w085",
             "n41w081", "n41w082", "n41w083", "n41w084", "n41w085",
             "n42w081", "n42w082", "n42w083", "n42w084", "n42w085"]

# save_directory = "/data"
save_directory = "/Users/kavanaughfrank/Desktop/OSGC/root/OSGC_API/data"

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

for tiff in tiff_list:
    # URL of the file to download
    url = f"https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/current/{tiff}/USGS_13_{tiff}.tif"

    # Send a GET request with stream=True to handle large files
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Try to extract the filename from the Content-Disposition header
        if "Content-Disposition" in response.headers:
            # Extract the filename from the header (if present)
            filename = response.headers["Content-Disposition"].split("filename=")[-1].strip('"')
        else:
            # Otherwise, fallback to the default filename or URL's last segment
            filename = os.path.basename(url)
        
        print("Started Download")
        tiff = tiff + ".tiff"
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
