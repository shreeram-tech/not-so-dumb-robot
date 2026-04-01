#include <ESP32Servo.h>

// Servo pin definitions
#define BASE_PIN 13
#define SHOULDER_PIN 12
#define ELBOW_PIN 14
#define GRIPPER_PIN 27

Servo baseServo;
Servo shoulderServo;
Servo elbowServo;
Servo gripperServo;

// Initial positions
int basePos = 90;
int shoulderPos = 90;
int elbowPos = 90;
int gripperPos = 90;

void setup() {
  Serial.begin(115200);
  
  // Allow ESP32 to allocate PWM channels automatically
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  // Attach servos
  baseServo.attach(BASE_PIN, 500, 2400);
  shoulderServo.attach(SHOULDER_PIN, 500, 2400);
  elbowServo.attach(ELBOW_PIN, 500, 2400);
  gripperServo.attach(GRIPPER_PIN, 500, 2400);
  
  // Move to initial positions
  updateServos();
  
  Serial.println("ESP32 Robotic Arm Ready");
}

void loop() {
  // Simple Serial Text Parsing Fallback
  // Format received from PC: "b:<angle>,s:<angle>,e:<angle>,g:<angle>\n"
  // Example: "b:90,s:45,e:135,g:0\n"
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    parseCommand(command);
  }
}

void parseCommand(String cmd) {
  // Parse simple formatted string
  int b_idx = cmd.indexOf("b:");
  int s_idx = cmd.indexOf("s:");
  int e_idx = cmd.indexOf("e:");
  int g_idx = cmd.indexOf("g:");
  
  if (b_idx != -1 && s_idx != -1 && e_idx != -1 && g_idx != -1) {
    basePos = cmd.substring(b_idx + 2, cmd.indexOf(',', b_idx)).toInt();
    shoulderPos = cmd.substring(s_idx + 2, cmd.indexOf(',', s_idx)).toInt();
    elbowPos = cmd.substring(e_idx + 2, cmd.indexOf(',', e_idx)).toInt();
    gripperPos = cmd.substring(g_idx + 2).toInt();
    
    // Constrain logic
    basePos = constrain(basePos, 0, 180);
    shoulderPos = constrain(shoulderPos, 0, 180);
    elbowPos = constrain(elbowPos, 0, 180);
    gripperPos = constrain(gripperPos, 0, 180); // 0 = closed, 180 = open (example)
    
    updateServos();
    Serial.println("OK");
  } else {
    Serial.println("Invalid format. Use: b:90,s:90,e:90,g:90");
  }
}

void updateServos() {
  baseServo.write(basePos);
  shoulderServo.write(shoulderPos);
  elbowServo.write(elbowPos);
  gripperServo.write(gripperPos);
}
