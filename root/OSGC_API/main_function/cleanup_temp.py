import os

def cleanup_temp_files(temp_files):
    """
    Remove temporary files from the filesystem.

    Args:
        temp_files (list of str): A list of file paths to be removed.

    Raises:
        Exception: If an error occurs during file removal other than FileNotFoundError.

    Notes:
        - If a file is not found, a message will be printed and the removal will be skipped.
        - Any other exceptions encountered during file removal will be caught and printed.
    """
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            print(f"{temp_file} not found. Skipping removal.")
        except Exception as e:
            print(f"Error removing {temp_file}: {e}")