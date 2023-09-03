# Arduino Python Audio Controller (APVC)

The Arduino Python Audio Controller (APVC) is a Python-based application that allows you to control the volume of multiple programs running on your computer using Arduino and potentiometers. It offers a custom-made solution to control audio levels effortlessly.

## Installation

To use APVC, you need to install the following Python libraries: comtypes pycaw pyyaml pywin32 pystray Pillow

```bash
pip install comtypes pycaw pyyaml pywin32 pystray Pillow

```

## Configuration

Before using APVC, you need to configure it with the following parameters in the `config.yaml` file:

-   **"port"**: Choose the COM port to which your Arduino is connected.

-   **"baud-rate"**: Set the baud rate to match the configuration on your Arduino.

-   **"apps"**: Enter the names of the programs you want to control with the potentiometers. You can organize applications into groups to manage audio settings efficiently. You can have multiple groups, and one potentiometer controls the entire group or the programs within that group.

    -   Ensure that the number of programs and groups listed in `apps` does not exceed the number of available potentiometers connected to your Arduino. Having more entries in `apps` than available potentiometers may lead to error.

    ```yaml
    port: Com6
    baud-rate: 9600
    apps:
        - master
        - game:
              - geometrydash.exe
              - terraria.exe
              - rust.exe
              - fortnite.exe
        - group:
              - opera.exe
              - discord.exe
    ```

In this example, there are two groups: "game" and "group." The "master" entry represents the overall system volume control. Adjusting the potentiometer assigned to "master" will affect the system's master volume. The "game" group includes multiple game-related programs, and adjusting the group's potentiometer will control the volumes of all games within that group. Similarly, the "group" contains multiple programs, and adjusting its potentiometer will control the volumes of all programs in that group.

## Arduino Configuration

1. Configure the `ArduinoCode.ino` according to your needs:

    - Set the number of potentiometers by changing `const byte numberOfPotentiometers = X;`, where `X` is the desired number.

    - Define the potentiometers' pins using the `potentiometersPins` array.

2. Upload the modified code to your Arduino.

## Usage

1. Connect your Arduino to your computer and ensure it has been programmed with the appropriate code as described in the "Arduino Configuration" section.

2. Configure the `config.yaml` file with the appropriate settings, as described in the "Configuration" section.

3. Run the Python script `APVC.py`. If the program doesn't work, make sure that the `config.yaml` file's location is same as the main script location.

4. Use the potentiometers connected to your Arduino to control the volume of the specified programs and groups.

    - **Master**: Adjusts the overall system volume.
    - **Groups**: Control volumes of specific groups of applications.
    - **Individual Applications**: Adjust volumes for specific applications.

Alternatively, you can use the Python script `APVC-console.py`:

1. Connect your Arduino to your computer and ensure it has been programmed with the appropriate code as described in the "Arduino Configuration" section.

2. Configure the `config.yaml` file with the appropriate settings, as described in the "Configuration" section.

3. Run the Python script `APVC-console.py` to launch the console-based application. This version does not include the `reload` function, and it operates in the console interface without a system tray icon.

## Features

APVC provides additional features:

-   **Running in the Background**: The main script runs silently in the background. You can access it through the system tray (hidden icons) on your taskbar.

-   **Reload Configuration**: Right-click on the system tray icon and select "Reload" to refresh the configuration from `config.yaml`.

-   **Exit**: To close the program entirely, right-click on the system tray icon and select "Exit."

## Note

Ensure you have the required hardware set up, including the potentiometers and Arduino, for APVC to work effectively.

---

Feel free to use and modify this project according to your needs. If you encounter any issues or have suggestions for improvements, please let me know by creating an issue in the GitHub repository.
