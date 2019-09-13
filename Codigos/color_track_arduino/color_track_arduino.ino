#include <Servo.h>
Servo servo1;
Servo servo2;
int pinServo1=5;
int SerUpPos;
int SerDownPos;
int pinServo2=6;
char Serialread;

void setup() {
  servo1.attach(pinServo1);
  servo2.attach(pinServo2);
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  SerUpPos = 75;
  SerDownPos = 90;
  servo1.write(SerUpPos);
  servo2.write(SerDownPos);
}

void loop() {
  if(Serial.available() > 0){
    Serialread = Serial.read();
    if(Serialread == '1'){
      SerUpPos += 1;
      servo1.write(SerUpPos);
    }
    else if(Serialread == '0'){
      SerUpPos -= 1;
      servo1.write(SerUpPos);
    }
    else if(Serialread == '3'){
      SerDownPos -= 1;
      servo2.write(SerDownPos);
    }
    else if(Serialread == '4'){
      SerDownPos += 1;
      servo2.write(SerDownPos);
    }
  }
}
