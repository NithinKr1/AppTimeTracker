import os
from pathlib import Path
import winshell
from win32com.client import Dispatch

def create_shortcut_to_startup(script_name, icon_name):
    startup_folder = Path(winshell.startup())
    script_path = Path(__file__).parent / script_name
    icon_path = Path(__file__).parent / icon_name
    shortcut_path = startup_folder / (script_path.stem + ".lnk")

    with winshell.shortcut(str(shortcut_path)) as shortcut:
        shortcut.path = str(script_path)
        shortcut.description = "Shortcut to start the application"
        shortcut.working_directory = str(script_path.parent)
        shortcut.icon_location = (str(icon_path), 0)  # Set the icon

if __name__ == "__main__":
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    batch_file_name = ".App.Time.Tracker. for Windows.bat"
    icon_file_name = "apptrackerlogo.ico"
    
    # Dynamically locate the batch file and icon
    create_shortcut_to_startup(batch_file_name, icon_file_name)
