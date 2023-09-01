from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import json
import serial
import win32con
import win32gui
import sys
import threading

# Function to hide the main application window
def hide_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

# Open the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

appList = []
configLen = len(config)

# Create a list of programs to control from the configuration file
for i in config["apps"]:
    appList.append(i)

port = config["port"]
baud_rate = config["baud-rate"]

ser = serial.Serial(port, baud_rate)

# Function that will be called in a separate thread
def background_task():
    while True:
        line = ser.readline()
        decoded_line = line.decode('utf-8', errors='ignore')
        parts = decoded_line.split('/')
        parts.pop()
        result = [float(part) / 100.0 for part in parts]

        for i in appList:
            if i == 'master':
                volume.SetMasterVolumeLevelScalar(result[appList.index("master")], None)

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                for j in appList:
                    if session.Process.name() == j:
                        app_volume = session.SimpleAudioVolume
                        app_volume.SetMasterVolume(result[appList.index(j)], None)

if __name__ == '__main__':
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Create a separate thread for the background task
    bg_thread = threading.Thread(target=background_task)
    bg_thread.start()

    # Hide the main window
    hide_window()

    # The program continues to run in the background in the main thread
    sys.exit()