from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import yaml
import serial
import win32con
import win32gui
import sys
import threading
import pystray
import PIL.Image
import os

# Define the paths for config file and icon file based on the script's directory
config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
icon_file_path = os.path.join(os.path.dirname(__file__), 'icon.png')

# Flag to control the main loop
running = True
appList = []


# Function to hide the main application window
def hide_window():
    # Get the handle to the foreground window and hide it
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


# Function to reload configuration
def reload():
    global appList, config
    with open(config_file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        appList.clear()
    for k in config["apps"]:
        appList.append(k)


reload()

# Get port and baud rate from the configuration
port = config["port"]
baud_rate = config["baud-rate"]

ser = serial.Serial(port, baud_rate)


# Function to handle tray icon events
def on_clicked(icon, item):
    global running
    if str(item) == "Exit":
        icon.stop()  # Stop the tray icon
        running = False  # Set the running flag to False
        sys.exit()  # Exit the program
    elif str(item) == "Reload":
        reload()


# Load the icon image
image = PIL.Image.open(icon_file_path)
icon = pystray.Icon("APVC", image, menu=pystray.Menu(
    pystray.MenuItem("Reload", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))


# Function that will be called in a separate thread
def background_task():
    while running:
        # Read data from the SerialPort
        line = ser.readline()
        decoded_line = line.decode('utf-8', errors='ignore')

        # Convert data from SerialPort to an array
        parts = decoded_line.split('/')
        parts.pop()
        result = [float(part) / 100.0 for part in parts if part.strip()]

        # Get a list of all audio sessions
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                for i in appList:
                    # Set volume for specific programs
                    if session.Process.name().lower() == str(i).lower():
                        app_volume = session.SimpleAudioVolume
                        app_volume.SetMasterVolume(result[appList.index(i)], None)
                    # Set master volume
                    if str(i).lower() == "master":
                        volume.SetMasterVolumeLevelScalar(result[appList.index("master")], None)

                    # Handling groups (group = game, same thing)
                    if isinstance(i, dict) and ('game' in i or 'group' in i):
                        app_name_list = i.get('game', []) + i.get('group', [])
                        for j in app_name_list:
                            if session.Process.name().lower() == str(j).lower():
                                app_volume = session.SimpleAudioVolume
                                app_volume.SetMasterVolume(result[appList.index(i)], None)
                            elif str(j).lower() == 'master':
                                volume.SetMasterVolumeLevelScalar(result[appList.index(i)], None)


if __name__ == '__main__':
    # Get the audio devices and interface for volume control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Create a separate thread for the background task
    bg_thread = threading.Thread(target=background_task)
    bg_thread.start()

    # Hide the main window
    hide_window()

    # Run the tray icon
    icon.run()
