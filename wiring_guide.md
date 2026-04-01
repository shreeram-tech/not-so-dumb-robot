# ESP32 Robotic Arm Wiring Guide

## Components Required
- 1x ESP32 Development Board
- 4x Servo Motors (SG90 or mg996r recommended)
- 1x INMP441 I2S Microphone (optional, if recording audio directly on ESP32)
- 1x External Power Supply for Servos (e.g., 5V 2A-3A minimum, do NOT power 4 servos directly from the ESP32 5V pin)

## Servos Wiring (Using external 5V power supply)
**IMPORTANT**: Connect the GND (Ground) of the external power supply to a GND pin on the ESP32 so they share a common ground.

1. **Base Servo**:
   - VCC -> External 5V
   - GND -> Shared GND
   - Signal -> ESP32 GPIO 13

2. **Shoulder Servo**:
   - VCC -> External 5V
   - GND -> Shared GND
   - Signal -> ESP32 GPIO 12

3. **Elbow Servo**:
   - VCC -> External 5V
   - GND -> Shared GND
   - Signal -> ESP32 GPIO 14

4. **Gripper Servo**:
   - VCC -> External 5V
   - GND -> Shared GND
   - Signal -> ESP32 GPIO 27

## INMP441 STT I2S Microphone Wiring (If implementing I2S audio recording)
- VDD -> ESP32 3.3V
- GND -> ESP32 GND
- L/R -> ESP32 GND (For left channel)
- WS (Word Select) -> ESP32 GPIO 15
- SCK (Serial Clock) -> ESP32 GPIO 2
- SD (Serial Data) -> ESP32 GPIO 4
