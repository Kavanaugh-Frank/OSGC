import time
import os
import io
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

Image.MAX_IMAGE_PIXELS = None  # Disable the limit

# List of .tiff file names of Ohio to download
# tiff_list = ["n39w082/", "n39w083/", "n39w084/", "n39w085/",
#              "n40w081/", "n40w082/", "n40w083/", "n40w084/", "n40w085/",
#              "n41w081/", "n41w082/", "n41w083/", "n41w084/", "n41w085/",
#              "n42w081/", "n42w082/", "n42w083/", "n42w084/", "n42w085/"]


tiff_list = ["n39w082/"]



current_dir = os.getcwd()
new_dir = "tiff"
# they need to be in the same parent directory for this script to save the images to the APIs folder of TIFF images
new_path = os.path.dirname(current_dir)
new_path = os.path.join(new_path, "OSGC_API", "tiff")

chrome_exe_path = os.path.join(current_dir, "chrome-win64", "chrome.exe")

# function to download and save a single TIFF file
def download_tiff(tiff):
    try:
       # options for chrome and the chromedriver
        chrome_options = Options()
        
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = chrome_exe_path

       
        # service = ChromeService(ChromeDriverManager().install())
        service = ChromeService(executable_path=os.path.join(current_dir, "chromedriver-win64", "chromedriver.exe"))

        
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # the URL format
        page_url = f"https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Elevation/13/TIFF/current/{tiff}"
        
        
        driver.get(page_url)

        # sleep to let the page load
        time.sleep(5)
        
        
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        # go to the link that has the TIFF download
        listing = soup.find('div', id="listing")
        tiff_url = listing.findAll("a")[3].get('href')

        
        r = requests.get(tiff_url, allow_redirects=True)

        # save the TIFF image
        img = Image.open(io.BytesIO(r.content))
        output_filename = f"{tiff.strip('/')}.tiff"
        print(output_filename)

        # saves the image in the TIFF folder located in the OSGC_API parent folder
        # only if OSGC_API and OSGC_webscraper have the same parent folder
        img.save(os.path.join(new_path, output_filename))
        
        # end the webdriver
        driver.quit()
    except Exception as e:
        print(f"Error downloading {tiff}: {e}")

# Use ThreadPoolExecutor to download files concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_tiff, tiff_list)
