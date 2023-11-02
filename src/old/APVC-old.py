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
import serial.tools.list_ports

# Define the paths for config file and icon file based on the script's directory
config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
icon_file_path = os.path.join(os.path.dirname(__file__), 'icon.png')
running = True
appList = []
port = None


# Function to hide the main application window
def hide_window():
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


# Function to handle tray icon events
def on_clicked(icon, item):
    global running
    if str(item) == "Exit":
        icon.stop()
        running = False
        sys.exit()
    elif str(item) == "Reload":
        reload()


# Finds arduino port
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for f_port in ports:
        if 'USB-SERIAL CH340' in f_port.description:
            return f_port.device
    return None


arduino_port = find_arduino_port()

try:
    if config["port"].lower() == "auto".lower():
        if arduino_port is not None:
            port = arduino_port
            print(f"Found arduino on port: {arduino_port}")
        else:
            print("Not found arduino.")
    else:
        port = config["port"]

except Exception as e:
    print(f"Error: {e}")
    sys.stdin.read()
    sys.exit(1)

baud_rate = config["baud-rate"]

try:
    ser = serial.Serial(port, baud_rate)
except Exception as e:
    print(f"Error: {e}, {serial.SerialException}")
    sys.stdin.read()
    sys.exit(1)

# Load the icon image
image = PIL.Image.open(icon_file_path)
global_icon = pystray.Icon("APVC", image, menu=pystray.Menu(
    pystray.MenuItem("Reload", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))


# Function that will be called in a separate thread
def background_task():
    while running:
        line = ser.readline()
        decoded_line = line.decode('utf-8', errors='ignore')

        parts = decoded_line.split('/')
        parts.pop()
        result = [float(part) / 100.0 for part in parts if part.strip()]

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                for i in appList:
                    if session.Process.name().lower() == str(i).lower():
                        app_volume = session.SimpleAudioVolume
                        app_volume.SetMasterVolume(result[appList.index(i)], None)
                    if str(i).lower() == "master":
                        volume.SetMasterVolumeLevelScalar(result[appList.index("master")], None)

                    if isinstance(i, dict) and ('game' in i or 'group' in i):
                        app_name_list = i.get('game', []) + i.get('group', [])
                        for j in app_name_list:
                            if session.Process.name().lower() == str(j).lower():
                                app_volume = session.SimpleAudioVolume
                                app_volume.SetMasterVolume(result[appList.index(i)], None)
                            elif str(j).lower() == 'master':
                                volume.SetMasterVolumeLevelScalar(result[appList.index(i)], None)


if __name__ == '__main__':
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    bg_thread = threading.Thread(target=background_task)
    bg_thread.start()

    hide_window()

    global_icon.run()
