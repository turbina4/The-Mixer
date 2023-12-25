import os
from ctypes import POINTER, cast
import sys
import pystray
import PIL.Image
import serial
import yaml
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial.tools.list_ports
import threading
from time import sleep

appList = []
running = True
config = {}

# Define the path for the config file based on the script's directory
config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
icon_file_path = os.path.join(os.path.dirname(__file__), 'icon.png')
folder_path = os.path.dirname(__file__)


def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for Port in ports:
        if 'USB-SERIAL CH340' in Port.description:
            return Port.device
    return None


arduino_port = find_arduino_port()


# Read config.yaml
def reload():
    global appList, config
    with open(f"{folder_path}\\config.yaml", 'r') as file:
        config = yaml.load(file, Loader = yaml.FullLoader)
    appList.clear()
    if "apps" in config:
        for h in config["apps"]:
            appList.append(h)


reload()


def on_clicked(icon, item):
    global running
    if str(item) == "Exit":
        running = False
        icon.stop()
        sys.exit()
    elif str(item) == "Open Config":
        if os.path.exists(f"{folder_path}\\config.yaml"):
            # print(f"Found config: {config_file_path}\\config.yaml")
            os.startfile(f"{folder_path}\\config.yaml")
    elif str(item) == "Reload":
        reload()
        check_config()


image = PIL.Image.open(icon_file_path)
global_icon = pystray.Icon("APVC", image, menu = pystray.Menu(
    pystray.MenuItem("Reload", on_clicked),
    pystray.MenuItem("Open Config", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))


def icon_thread():
    global_icon.run()


icon_thread = threading.Thread(target = icon_thread)
icon_thread.start()


def check_config():
    if all(key in config for key in ["port", "baud-rate", "apps"]):

        # Variables
        port = None
        ser = None
        try:
            # Get port and baud rate from the configuration
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

        baud_rate = config["baud-rate"]

        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
        except Exception as e:
            ser.close()
            print(f"Error: {e}, {serial.SerialException}")

        print(ser)
        # Get the audio devices and interface for volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Populate the appList with applications from the config
        for k in config["apps"]:
            appList.append(k)

        sleep(.25)
        while running:
            # Read data from the SerialPort
            try:
                line = ser.readline()
            except Exception as e:
                print(e)
                line = None
            decoded_line = line.decode('utf-8', errors = 'ignore')
            result = []
            try:
                # Convert data from SerialPort to an array
                parts = decoded_line.split('|')
                result = [round(float(part) / 1023.0, 2) for part in parts if part.strip()]
            except ValueError as e:
                print(f'!Error: {e}, Failed to convert.')

            try:
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

                            # Handling groups and games (group = game, same thing)
                            if isinstance(i, dict) and ('game' in i or 'group' in i):
                                app_name_list = i.get('game', []) + i.get('group', [])
                                for j in app_name_list:
                                    if session.Process.name().lower() == str(j).lower():
                                        app_volume = session.SimpleAudioVolume
                                        app_volume.SetMasterVolume(result[appList.index(i)], None)
                                    elif str(j).lower() == 'master':
                                        volume.SetMasterVolumeLevelScalar(result[appList.index(i)], None)
            except Exception as e:
                print(f'!ERROR: {e}, Failed to change volume')
        else:
            ser.close()


check_config()
