# ESP32 BLE Wand

A wand that transmits accelerometer data (captured by an STM32) to a host machine over Bluetooth Low Energy via an ESP32. Features a host application that draws the wand movements to the terminal.

## Hardware

### ESP-WROOM-32
voltage: 3-5V
[datasheet]()

### STM32F446RE
voltage: 3-5V
[datasheet]()


### MPU-6500 Accelerometer
voltage: 3-5V
[datasheet](https://www.alldatasheet.com/datasheet-pdf/view/1140874/TDK/MPU-6500.html)
[register map](https://github.com/bolderflight/invensense-imu/blob/main/docs/MPU-6500-Register-Map.pdf)

## Block Diagram

<div width="100%">
  <img align="center" src="media/BlockDiagram.png" width="100%"/>
</div>

## Circuit Diagram

<div width="100%">
  <img align="center" src="media/circuit.png" width="100%"/>
</div>

## Host side application

Python Tui application that communicates with the ESP32 over BLE and draws the
magic wand's movements to the screen.

Run will `make app` or `python3.14 app/app.py`

### Dependencies

* Python 3.14
  * bleak
  * shutil
  * curses
* BlueZ

## ESP32

### Dependencies

* ArduinoIDE
* esp32 board package by Espressif Systems
* ESP32 BLE Arduino

### Compilation

Use Arduino IDE with the ESP32 Dev Module from Espressif to compile and flash.

## STM32

### Dependencies

### Compilation

## BlueTooth Protocol
