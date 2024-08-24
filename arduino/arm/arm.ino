#include <Servo.h>

#define SERVO_PIN_1 4
#define SERVO_PIN_2 5

Servo servo1;
Servo servo2;

void setup() {
  servo2.attach(SERVO_PIN_2);
  delay(3000);
}

void loop() {
  servo2.write(0);
  delay(5000);
  servo2.write(180);
  delay(5000);
}
