import serial
import time
import requests
import json
import threading
import sys

# -------- CONFIGURATION --------
# Replace with your ESP32's actual COM/Serial port
SERIAL_PORT = 'COM4' # e.g., '/dev/ttyUSB0' on Linux/Mac or 'COMx' on Windows
BAUD_RATE = 115200

# Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"# The Local LLM Model to use
MODEL_NAME = "gemma:2b" # Requires you to pull gemma:2b or similar locally in Ollama

# -------------------------------

# Initialize Serial
try:
    esp32 = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Wait for ESP32 to reboot
    print(f"Connected to ESP32 on {SERIAL_PORT}")
except Exception as e:
    print(f"FAILED to connect to ESP32: {e}")
    print("Continuing in test mode. Commands won't be sent to hardware.")
    esp32 = None

def send_command(base, shoulder, elbow, gripper):
    cmd = f"b:{base},s:{shoulder},e:{elbow},g:{gripper}\n"
    print(f"Sending to ESP32: {cmd.strip()}")
    if esp32:
        esp32.write(cmd.encode('utf-8'))
        response = esp32.readline().decode('utf-8').strip()
        print(f"ESP32 Response: {response}")

def ask_llm(user_prompt):
    """
    Asks Gemma to convert user text like "pick up the item" 
    into a JSON response with target angles.
    """
    system_prompt = '''You are the controller for a 4-degree-of-freedom robotic arm (Base, Shoulder, Elbow, Gripper).
Angles are in degrees from 0 to 180.
- Base: 0 to 180 (90 is center, 0 right, 180 left)
- Shoulder: 0 to 180 (90 is up, <90 is forward, >90 is back)
- Elbow: 0 to 180 (90 is straight out, <90 is bend down, >90 is bend up)
- Gripper: 0 to 180 (180 is open, 0 is fully closed)

Current Position ranges: b:90, s:90, e:90, g:180.

A user will give a command. You MUST respond ONLY with valid JSON. Do not include any other text.
Format:
{
  "base": <int>,
  "shoulder": <int>,
  "elbow": <int>,
  "gripper": <int>
}

Example inputs and outputs:
Input: "turn left" -> {"base": 180, "shoulder": 90, "elbow": 90, "gripper": 180}
Input: "pick up the item" -> {"base": 90, "shoulder": 45, "elbow": 45, "gripper": 0}
Input: "open hands" -> {"base": 90, "shoulder": 90, "elbow": 90, "gripper": 180}
'''

    prompt = system_prompt + "\nUser command: " + user_prompt

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        output = response.json().get('response', '{}')
        
        # Parse output JSON
        data = json.loads(output)
        return data.get("base", 90), data.get("shoulder", 90), data.get("elbow", 90), data.get("gripper", 90)
    except Exception as e:
        print(f"LLM Error: {e}")
        return None


def main():
    print("=== ESP32 + Gemma 3 Offline Robotic Arm Controller ===")
    print("Type your commands.")
    
    while True:
        try:
            user_input = input("\nEnter command ['q' to quit]: ").strip()
            
            if user_input.lower() == 'q':
                break
            else:
                text_command = user_input
                
            if text_command:
                print(f"\nSending to LLM: '{text_command}'")
                result = ask_llm(text_command)
                
                if result:
                    b, s, e, g = result
                    send_command(b, s, e, g)
                else:
                    print("Could not parse LLM response. Try another command.")
                    
        except KeyboardInterrupt:
            break
            
    if esp32:
        esp32.close()
    print("Exited.")

if __name__ == "__main__":
    main()
