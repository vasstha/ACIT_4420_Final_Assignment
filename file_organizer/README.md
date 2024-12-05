
# File Organizer

## Overview
File Organizer is a Python-based application designed to declutter and organize files in a directory. It categorizes files into subfolders based on their types (e.g., images, documents, videos) and provides a user-friendly graphical interface for ease of use. The application can also be run via the command line for advanced users.

## Features
### Automated File Organization:
- Categorizes files into predefined folders based on their extensions.
- Handles unsupported file types by placing them in a "Miscellaneous" folder.

### Graphical User Interface (GUI):
- Intuitive interface for selecting folders and initiating the organization process.
- Displays success or error notifications.

### Command-Line Support:
- Execute file organization tasks directly from the terminal with optional arguments.

### Cross-Platform Compatibility:
- Works on Windows, macOS, and Linux (via source installation).

## Requirements
### Supported Systems
- **Windows 10/11**: Executable provided.
- **macOS and Linux**: Source installation.

### Dependencies
- **Python 3.8 or later**
- Libraries:
  - Standard Python modules like `os`, `shutil`, and `logging`

## Installation
### Windows (Executable Installation)
1. **Download the ZIP File**:
   - Download the `FileOrganizer.zip` file from the [Releases page](#).
2. **Extract the ZIP File**:
   - Right-click the ZIP file and select "Extract All".
   - Open the extracted folder.
3. **Run the Application**:
   - Double-click the `main.exe` file to launch the application.
   - Follow the instructions in the GUI to organize files.

### Source Installation (macOS/Linux/Windows)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vasstha/ACIT_4420_Final_Assignment.git
   cd FileOrganizer
   ```
2. **Install Dependencies**:
   - **(Optional)** Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Linux/macOS
     venv\Scripts\activate  # On Windows
     ```
   - Install required libraries:
     ```bash
     pip install .
     ```

3. **Run the Application**:
   - **GUI Mode**:
     ```bash
     python main.py
     ```
   - **Command-Line Mode**:
     ```bash
     python main.py "C:\path\to\your\folder"
     ```

## Usage Instructions
### GUI Mode:
1. Open the application (`main.exe` or via Python).
2. Select a folder to organize using the GUI.
3. Click **Organize Files** to start the process.
4. View the success message once the organization is complete.

### Command-Line Mode:
1. Open a terminal or command prompt.
2. Run the following command:
   ```bash
   python main.py "C:\path\to\your\folder"
   ```

## Contributing
Contributions are welcome! If you have ideas for improvement or encounter bugs, feel free to:
- Open an issue on the [GitHub repository](https://github.com/vasstha/ACIT_4420_Final_Assignment).
- Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or support, feel free to contact me:
- **Name**: Vaskar Shrestha
- **Email**: [vashr0444@oslomet.no](mailto:vashr0444@oslomet.no)

