import os

def cleanup_temp_files(temp_files):
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            print(f"{temp_file} not found. Skipping removal.")
        except Exception as e:
            print(f"Error removing {temp_file}: {e}")