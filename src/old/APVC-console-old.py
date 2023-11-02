import os
from ctypes import POINTER, cast

import serial
import yaml
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial.tools.list_ports

try:
    def find_arduino_port():
        ports = serial.tools.list_ports.comports()
        for Port in ports:
            if 'USB-SERIAL CH340' in Port.description:
                return Port.device
        return None


    arduino_port = find_arduino_port()

    # Define the path for the config file based on the script's directory
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    # Read config.yaml
    with open(config_file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # Variables
    appList = []
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
        print(f"Error: {e}, BŁĄD AUTO")

    baud_rate = config["baud-rate"]
    print("test1")
    try:
        ser = serial.Serial(port, baud_rate)
    except Exception as e:
        print(f"Error: {e}, {serial.SerialException}, BŁĄD SERIAL")

    # Get the audio devices and interface for volume control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("test2")
    # Populate the appList with applications from the config
    for k in config["apps"]:
        appList.append(k)
    print(ser, port, baud_rate)
    while True:
        # Read data from the SerialPort
        line = ser.readline()
        decoded_line = line.decode('utf-8', errors='ignore')
        print("test4")
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
except Exception as e:
    print(f'Błąd: ${e}')
    input("Press Enter to exit")
