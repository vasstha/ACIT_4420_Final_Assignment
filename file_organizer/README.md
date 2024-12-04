# File Organizer

## Overview
The **File Organizer** is a Python-based tool designed to declutter and organize files in a selected directory. It categorizes files into subfolders based on their file types (e.g., images, documents, videos) for better organization and ease of access. The tool includes a graphical user interface (GUI) and can also be run via the command line.

---

## Features
- **File Type-Based Organization**:
  - Automatically sorts files into predefined categories such as Images, Documents, Videos, and more.
  - Handles various file types based on extensions defined in a configuration file.
- **GUI Support**:
  - User-friendly interface for selecting directories and organizing files.
- **Command-Line Support**:
  - Allows running the tool with a specified directory directly from the terminal.
- **Error Logging**:
  - All errors are logged in a dedicated log file (`file_organizer.log`) for debugging purposes.

---

## File Descriptions

### `config.py`
- Contains a dictionary `FILE_TYPE_MAP` that maps file extensions to their respective categories.
- Example:
  ```python
  FILE_TYPE_MAP = {
      "Images": [".jpg", ".jpeg", ".png", ".gif"],
      "Documents": [".txt", ".pdf", ".docx"],
      ...
  }
