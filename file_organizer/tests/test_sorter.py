import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sorter import organize_files, determine_folder
from unittest.mock import patch
from src.gui import launch_gui
import logging
from src.logger import log_error
from main import main
from src.utils import log_function_call
from io import StringIO

@pytest.fixture
def setup_test_directory(tmp_path):
    files = ["test.txt", "image.jpg", "music.mp3", "code.py"]
    for file in files:
        (tmp_path / file).write_text("dummy content")
    return tmp_path

def test_organize_files(setup_test_directory):
    organize_files(setup_test_directory)
    assert (setup_test_directory / "Documents").exists()
    assert (setup_test_directory / "Images").exists()
    assert (setup_test_directory / "Audio").exists()

def test_sorter_file_not_found():
    with pytest.raises(FileNotFoundError, match="Directory 'non_existent_directory' does not exist"):
        organize_files("non_existent_directory")

def test_determine_folder():
    assert determine_folder(".txt") == "Documents"
    assert determine_folder(".jpg") == "Images"
    assert determine_folder(".unknown") == "Miscellaneous"

"""
@patch("tkinter.filedialog.askdirectory", return_value="mock_directory")
@patch("sorter.organize_files")
def test_gui_flow(mock_organize, mock_ask):
    with patch("tkinter.Tk.mainloop", side_effect=SystemExit):  # Prevent infinite GUI loop
        try:
            launch_gui()
        except SystemExit:
            pass

    # Manually trigger select_directory to ensure the flow
    from gui import select_directory
    select_directory()

    # Assert that askdirectory was called only once
    mock_ask.assert_called_once_with()
    mock_organize.assert_not_called()  # Organize should not be called without a valid trigger
"""

@log_function_call
def sample_function(x, y):
    return x + y

def test_logging(caplog):
    with caplog.at_level(logging.ERROR):
        log_error("Test error")
    assert "Test error" in caplog.text

    with caplog.at_level(logging.INFO):
        result = sample_function(2, 3)
        assert result == 5
        assert "Function sample_function called with args: (2, 3), kwargs: {}" in caplog.text

"""
def test_main(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "mock_directory"])
    with patch("sorter.organize_files") as mock_organize:
        with patch("os.path.exists", return_value=True):  # Mock directory existence
            main()
            mock_organize.assert_called_once_with("mock_directory")


def test_main_exception(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "mock_directory"])
    with patch("sorter.organize_files", side_effect=Exception("Test Exception")) as mock_organize:
        with patch("logger.log_error") as mock_log_error:
            with patch("os.path.exists", return_value=True):  # Mock directory existence
                main()
                mock_organize.assert_called_once_with("mock_directory")
                mock_log_error.assert_called_once_with("Test Exception")

def test_main_output(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py", "mock_directory"])
    with patch("sorter.organize_files") as mock_organize:
        with patch("os.path.exists", return_value=True):  # Mock directory existence
            main()
            captured = capsys.readouterr()
            assert "Files organized successfully!" in captured.out


"""

def test_main_invalid_directory(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "non_existent_directory"])
    with patch("logger.log_error") as mock_log_error:
        main()
        mock_log_error.assert_not_called()



