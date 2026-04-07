# ESP32 BLE Wand

A wand that transmits accelerometer data (captured by an STM32) to a host machine over Bluetooth Low Energy via an ESP32. Features a host application that draws the wand movements to the terminal.

## Hardware

### ESP-WROOM-32
voltage: 3-5V
[datasheet](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.pdf)

### STM32F446RE
voltage: 3-5V
[datasheet](https://www.st.com/content/ccc/resource/technical/document/datasheet/65/cb/75/50/53/d6/48/24/DM00141306.pdf/files/DM00141306.pdf/jcr:content/translations/en.DM00141306.pdf)


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

Run `make app` or `python3.14 app/app.py`

### Dependencies

* Python 3.14
  * bleak
  * shutil
  * curses
* BlueZ

## ESP32

Handles device-side Bluetooth Low Energy commincation.

### Dependencies

* ArduinoIDE
* esp32 board package by Espressif Systems
* ESP32 BLE Arduino

### Compilation

Use Arduino IDE with the ESP32 Dev Module from Espressif to compile and flash.

## STM32

Handles MPU6500 set up and communication.

### Dependencies

* STM32CubeMX
* Make
* arm-none-eabi-gcc
* st-link

### Compilation

Run `make stm32` for compiling the source, and `make stm32-flash` for flashing
the binary to the stm32 using st-link.
