# Arduino Volume Controller

## Overview

The Arduino Volume Controller is a Python-based application that enables you to control the volume of multiple programs running on your computer using Arduino and potentiometers. It is similar to Arduino DEEJ but is a custom-made solution in Python.

## Configuration

Before using the Arduino Volume Controller, you need to configure it with the following parameters:

-   **"apps"**: Enter the names of the programs you want to control with the potentiometers. Ensure that the number of programs does not exceed the number of potentiometers you have.

-   **"port"**: Choose the COM port to which your Arduino is connected.

-   **"baud-rate"**: Set the baud rate to match the configuration on your Arduino.

-   If you want to control master volume enter a **_"master"_** in **"apps"**.

## Installation

To use the Arduino Volume Controller, you need to install the following Python libraries:

```
pip install pycaw
pip install pyserial
```

## Usage

1. Connect your Arduino to your computer.

2. Configure the `config.json` file with the appropriate settings.

3. Run the Python script. If the program doesn't work, make sure that the `config.json` file's location is correctly specified in the script.

4. Use the potentiometers connected to your Arduino to control the volume of the specified programs.

## Note

Make sure you have the required hardware set up, including the potentiometers and Arduino, for this controller to work effectively.
