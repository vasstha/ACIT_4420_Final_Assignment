import os
import shutil
from config import FILE_TYPE_MAP

def organize_files(directory):
    """
    Organizes files in the specified directory based on file types.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):  # Skip directories
            continue

        _, extension = os.path.splitext(filename)
        target_folder = determine_folder(extension)
        target_path = os.path.join(directory, target_folder)

        os.makedirs(target_path, exist_ok=True)
        shutil.move(file_path, os.path.join(target_path, filename))

def determine_folder(extension):
    """
    Determines the folder name based on the file extension.
    """
    for folder, extensions in FILE_TYPE_MAP.items():
        if extension.lower() in extensions:
            return folder
    return "Miscellaneous"
