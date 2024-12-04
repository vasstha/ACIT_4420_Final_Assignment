import os
import sys
from file_organizer.gui import launch_gui
from file_organizer.sorter import organize_files
from file_organizer.logger import log_error


def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return
        try:
            organize_files(directory)
            print("Files organized successfully!")
        except Exception as e:
            log_error(e)
            print(f"Error: {e}")
    else:
        launch_gui()

if __name__ == "__main__":
    main()

