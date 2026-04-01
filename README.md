# Offline ESP32 Robotic Arm Controlled by Local LLM

This project consists of a 4-degrees-of-freedom robotic arm (Base, Shoulder, Elbow, Gripper) controlled by an ESP32 microcontroller, which receives commands from a Python script running on a PC. The PC script utilizes a local Large Language Model (LLM) through Ollama to translate natural language commands into specific joint angles.

## Project Structure

- `arduino_arm/arduino_arm.ino`: The main firmware for the ESP32. It initializes the servo motors, listens for serial commands from the PC, parses the incoming text, and moves the servos to the target angles.
- `pc_controller/app.py`: A Python script that acts as the bridge between the user, the local LLM, and the ESP32. It prompts the user for text commands, queries a local LLM (Gemma:2b via Ollama) to convert the text into JSON-formatted servo angles, and sends these angles to the ESP32 via Serial.
- `wiring_guide.md`: A detailed guide on how to wire the ESP32 to the servo motors and external power supply.

## How It Works

1. **User Input**: You run `app.py` on your PC and type a natural language command like "pick up the item" or "turn left".
2. **LLM Processing**: The Python script sends your text command along with a specific system prompt to a locally running instance of Ollama (using the `gemma:2b` model). The system prompt instructs the LLM to output a precise JSON object containing angles (0 to 180 degrees) for the `base`, `shoulder`, `elbow`, and `gripper`.
3. **Serial Communication**: Once the script receives the JSON from the LLM, it extracts the target angles and formats them into a compact string like `b:90,s:45,e:45,g:0\n`. It sends this string over USB Serial to the connected ESP32.
4. **Hardware Execution**: The ESP32 constantly reads its Serial buffer. When a full command line is received, it splits the string, extracts the target angles, applies boundary constraints (0-180), and updates the PWM signals using the `ESP32Servo` library to physically move the arm to the desired position.

## Setup

1. **Hardware**: Wire the ESP32 and servos according to `wiring_guide.md`. Ensure you use a dedicated external 5V power supply for the servos and share the ground with the ESP32.
2. **ESP32 Firmware**: Open `arduino_arm.ino` in the Arduino IDE, install the `ESP32Servo` library by Kevin Harrington, and upload the code to your ESP32 board. Note the COM port used.
3. **Local LLM**: Install [Ollama](https://ollama.com/) on your PC and pull the Gemma 2B model by running `ollama run gemma:2b` in your terminal.
4. **Python Dependencies**: Navigate to the `pc_controller` directory and install dependencies if necessary (e.g., `pip install requests pyserial`).

## How to Run

Follow these steps every time you want to operate the robotic arm:

1. **Start Ollama**: Make sure Ollama or the Ollama service is running in the background.
2. **Configure Port**: Edit `app.py` in the `pc_controller` directory. Update the `SERIAL_PORT` variable to match your connected ESP32's actual COM port (e.g., `'COM4'` or `'/dev/ttyUSB0'`).
3. **Run the Controller**:
   - Open a terminal and navigate to the `pc_controller` directory.
   - Run the script:
     ```bash
     python app.py
     ```
4. **Issue Commands**: Once the script is running, type natural language commands into the terminal prompt (e.g., "pick up the item", "turn left") and watch the robotic arm respond.
