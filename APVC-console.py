from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import yaml
import serial
import os

# Define the path for the config file based on the script's directory
config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

# Read config.yaml
with open(config_file_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Variables
appList = []
port = config["port"]
baud_rate = config["baud-rate"]

# Get the audio devices and interface for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Populate the appList with applications from the config
for k in config["apps"]:
    appList.append(k)

# Set the serial port
ser = serial.Serial(port, baud_rate)

while True:
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
                    appVolume = session.SimpleAudioVolume
                    appVolume.SetMasterVolume(result[appList.index(i)], None)
                # Set master volume
                if str(i).lower() == "master":
                    volume.SetMasterVolumeLevelScalar(result[appList.index("master")], None)

                # Handling groups and games (group = game, same thing)
                if isinstance(i, dict) and ('game' in i or 'group' in i):
                    app_name_list = i.get('game', []) + i.get('group', [])
                    for j in app_name_list:
                        if session.Process.name().lower() == str(j).lower():
                            appVolume = session.SimpleAudioVolume
                            appVolume.SetMasterVolume(result[appList.index(i)], None)
                        elif str(j).lower() == 'master':
                            volume.SetMasterVolumeLevelScalar(result[appList.index(i)], None)
