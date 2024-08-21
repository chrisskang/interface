// RANGE : 440 - 2465
// Center : 1550



#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// 서보 모터의 최소 및 최대 펄스 길이를 정의합니다.
#define SERVOMIN  90   // 440 µsec
#define SERVOMAX  1385 // 2465 µsec

#define USMIN  440  // 최소 펄스 길이 (440 µsec)
#define USMAX  2465 // 최대 펄스 길이 (2465 µsec)

#define SERVO_FREQ 50 // 서보 주파수 설정 (50 Hz)

uint8_t servonum = 1;

void setup() {
  Serial.begin(115200);
  pinMode(6,OUTPUT);
  digitalWrite(6,LOW);
//  pinMode(9,OUTPUT);
//  pinMode(10,OUTPUT);
//
//  digitalWrite(9,HIGH);
//  digitalWrite(10,HIGH);
  
  Serial.println("E");
  delay(500);
  pwm.begin();
  //pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);
  
  delay(10);
  
  Serial.println("Enter pulse length in microseconds (440-2465):");
}



void loop() {
  Serial.println("hihg");
  pwm.setPWM(0,4096,0);
  delay(1000);
  Serial.println("low");
  pwm.setPWM(0,0,4096);
  delay(1000);
}
