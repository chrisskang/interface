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
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);

  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  
  
  delay(500);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);
  
  delay(10);

  Serial.println("Enter pulse length in microseconds (440-2465):");
}

void setServoPulse(uint8_t n, int pulse) {
  double pulselength = 1000000.0 / SERVO_FREQ / 4096.0; // 1,000,000 us per second / frequency / 12 bits resolution
  int pulseval = pulse / pulselength;
  Serial.print("Pulse value: ");
  Serial.println(pulseval);
  pwm.setPWM(1, 0, pulseval);
  pwm.setPWM(14, 0, pulseval);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // 시리얼 모니터에서 문자열 입력 받기
    input.trim(); // 입력된 문자열의 공백 제거
    int pulselen = input.toInt(); // 문자열을 정수로 변환

    Serial.print("Received input: ");
    Serial.println(input);
    Serial.print("Converted to integer: ");
    Serial.println(pulselen);

    if (pulselen >= USMIN && pulselen <= USMAX) {
      setServoPulse(servonum, pulselen);
      Serial.print("Pulse length set to: ");
      Serial.print(pulselen);
      Serial.println(" us");
    } else {
      Serial.println("Invalid pulse length. Enter a value between 440 and 2465.");
    }
  }
}
