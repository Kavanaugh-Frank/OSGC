import os, sys

# define the volume directory that is inside the container
# volume_directory = "/data"
volume_directory = os.path.join(os.getcwd(), 'data')
# define the holder directory that is inside the container
# holder_directory = "/holder"
# Check if the script is running as a PyInstaller executable
if hasattr(sys, '_MEIPASS'):
    # Get the base path for PyInstaller executables
    base_path = sys._MEIPASS
else:
    # Get the base path for normal script execution
    base_path = os.getcwd()

# Define the holder directory relative to the base path
holder_directory = os.path.join(base_path, 'holder')

# Make the directory if it does not exist
os.makedirs(holder_directory, exist_ok=True)