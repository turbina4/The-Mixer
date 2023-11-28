# Arduino Python Volume Controller (APVC)

The Arduino Python Audio Controller (APVC) is a Python-based application that allows you to control the volume of multiple programs running on your computer using Arduino and potentiometers. It offers a custom-made solution to control audio levels effortlessly.
**WORKS ONLY WITH WINDOWS**

-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Arduino Configuration](#arduino-configuration)
-   [Usage](#usage)
-   [Features](#features)
-   [Autostart with Windows](#Autostart-with-Windows)

## Installation

Download APVC-download.zip -> Unzip it -> Enjoy

It may be necessary to install `CH340` drivers.

## Configuration

Before using APVC, you need to configure it with the following parameters in the `config.yaml` file:

-   **"port"**: Choose the COM port to which your Arduino is connected.

-   **"port: auto"**: Program automatically selects port. Might not work with more than 1 arduino connected to the computer

-   **"baud-rate"**: Set the baud rate to match the configuration on your Arduino.

-   **"apps"**: Enter the names of the programs you want to control with the potentiometers. You can organize applications into groups to manage audio settings efficiently. You can have multiple groups, and one potentiometer controls the entire group or the programs within that group.

    -   **Master**: Adjusts the overall system volume.
    -   **Groups**: Control volumes of specific groups of applications.
    -   **Individual Applications**: Adjust volumes for specific applications.

    -   Ensure that the number of programs and groups listed in `apps` does not exceed the number of available potentiometers connected to your Arduino. Having more entries in `apps` than available potentiometers may lead to error.

    **Example**

    ```yaml
    port: Com6
    baud-rate: 9600
    apps:
        - master
        - spotify.exe
        - game:
              - geometrydash.exe
              - terraria.exe
              - rustclient.exe
              - fortnite.exe
        - discord.exe
        - group:
              - opera.exe
              - chrome.exe
    ```

    **Different example**

    ```yaml
    port: auto
    baud-rate: 9600
    apps:
        - master
        - opera.exe
        - discord.exe
        - group:
              - spotify.exe
              - AMPLibraryAgent.exe
        - game:
              - geometrydash.exe
              - albion-online.exe
              - rustclient.exe
              - robloxplayerbeta.exe
              - cs2.exe
    ```

## Arduino Configuration

1. Configure the `arduino_code.ino` according to your needs:

    - Set the number of potentiometers by changing `const int NUM_SLIDERS = X;`, where `X` is the desired number.

    - Define the potentiometers' pins using the `const int analogInputs` array.

    **Example**

    ```
    const int NUM_SLIDERS = 5;
    const int analogInputs[NUM_SLIDERS] = {A0, A1, A2, A3, A4};
    ```

2. Upload the modified code to your Arduino.

> Arduino code is same as [deej arduino code](https://github.com/omriharel/deej)

## Usage

1. Connect your Arduino to your computer and ensure it has been programmed with the appropriate code as described in the "Arduino Configuration" section.

2. Run the `APVC.exe` or `APVC-Main.exe`. If the program doesn't work, check `config.yaml`. You can do this by clicking `Change config` in APVC options. If you change config make sure that you reload program by clicking `reload` in APVC options.

3. Use the potentiometers connected to your Arduino to control the volume of the specified programs and groups.

`All option are in the system tray icon options.`

## Features

APVC provides additional features:

-   **Running in the Background**: The main script runs silently in the background. You can access it through the system tray (hidden icons) on your taskbar.

-   **Open Config**: Right-click on the system tray icon and select "Open Config" to open and edit `config.yaml`.

-   **Reload Configuration**: Right-click on the system tray icon and select "Reload" to refresh the configuration.

-   **Exit**: To close the program entirely, right-click on the system tray icon and select "Exit."

## Autostart with Windows

If you want APVC to start automatically with Windows, you can add a shortcut to the program in the startup folder. Here's how:

1. Press `Win + R` to open the Run dialog.
2. Type `%appdata%\Microsoft\Windows\Start Menu\Programs\Startup` and press Enter.
3. Copy the shortcut of `APVC.exe` into this folder.

Now, APVC will launch automatically when you start your computer.

## Note

Ensure you have the required hardware set up, including the potentiometers and Arduino, for APVC to work effectively.

---

Feel free to use and modify this project according to your needs. If you encounter any issues or have suggestions for improvements, please let me know by creating an issue in the GitHub repository.
