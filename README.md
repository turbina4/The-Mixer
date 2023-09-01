# Arduino Volume Controller

The Arduino Volume Controller is a Python-based application that enables you to control the volume of multiple programs running on your computer using Arduino and potentiometers. It is similar to Arduino DEEJ but is a custom-made solution in Python.

## Configuration

Before using the Arduino Volume Controller, you need to configure it with the following parameters:

-   **"apps"**: Enter the names of the programs you want to control with the potentiometers. Ensure that the number of programs does not exceed the number of potentiometers you have.

-   **"port"**: Choose the COM port to which your Arduino is connected.

-   **"baud-rate"**: Set the baud rate to match the configuration on your Arduino.

-   If you want to control the master volume, enter a **_"master"_** in **"apps"**.

## Installation

To use the Arduino Volume Controller, you need to install the following Python libraries:

```
pip install pycaw
pip install pyserial
```

## Arduino Configuration

1. Upload the `ArduinoCode.ino` file to your Arduino board.

2. Configure the Arduino code according to your needs.

    - Set the number of potentiometers by changing `const byte numberOfPotentiometers = X;`, where `X` is the desired number.

    - Define the potentiometers' pins using the `potentiometersPins` array.

3. Upload the modified code to your Arduino.

## Usage

1. Connect your Arduino to your computer.

2. Configure the `config.json` file with the appropriate settings.

3. Run the Python script `main.py`. If the program doesn't work, make sure that the `config.json` file's location is correctly specified in the script.

4. Use the potentiometers connected to your Arduino to control the volume of the specified programs.

## Background Task

In addition to `main.py`, there is a background task script, `main_background.py`, that continuously monitors the potentiometers' values and updates the volume accordingly. This script runs in the background, allowing you to control the volume without the main window being visible.

## Note

Make sure you have the required hardware set up, including the potentiometers and Arduino, for this controller to work effectively.
