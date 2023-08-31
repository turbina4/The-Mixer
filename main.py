from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import json
import serial

# Read config.json
with open('config.json', 'r') as file:
    config = json.load(file)

appList = []
configLen = len(config)

# Create a list of programs to control from the configuration file
for i in config["apps"]:
    appList.append(i)

port = config["port"]
baud_rate = config["baud-rate"]

# Set up the serial port
ser = serial.Serial(port, baud_rate)

# Main part of the program
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    # Read data from the serial port
    line = ser.readline()
    decoded_line = line.decode('utf-8', errors='ignore')

    # Convert data from the serial port to an array
    parts = decoded_line.split('/')
    parts.pop()
    result = [float(part) / 100.0 for part in parts]

    # Set the master volume
    for i in appList:
        if i == 'master':
            volume.SetMasterVolumeLevelScalar(result[appList.index("master")], None)

    # Set volumes for individual programs
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            for j in appList:
                if session.Process.name() == j:
                    appVolume = session.SimpleAudioVolume
                    appVolume.SetMasterVolume(result[appList.index(j)], None)

    print(result)
