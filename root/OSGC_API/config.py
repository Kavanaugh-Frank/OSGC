import os

# define the volume directory that is inside the container
# volume_directory = "/data"
volume_directory = os.path.join(os.getcwd(), 'data')
# define the holder directory that is inside the container
# holder_directory = "/holder"
holder_directory = os.path.join(os.getcwd(), 'holder')
# make the directory if it does not exist in the container
os.makedirs(holder_directory, exist_ok=True)