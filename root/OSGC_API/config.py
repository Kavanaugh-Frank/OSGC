import os

# define the volume directory that is inside the container
volume_directory = "/data"
# define the holder directory that is inside the container
holder_directory = "/holder"
# make the directory if it does not exist in the container
os.makedirs(holder_directory, exist_ok=True)