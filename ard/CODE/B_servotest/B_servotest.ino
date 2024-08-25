#define mosfetA A2
#define mosfetB A3
#define currentA A1
#define currentB A0
#define pwmA 9
#define pwmB 10
#include <Servo.h>

Servo myServo;

void setup() {
  // 서보 모터 핀 연결 (예: 핀 9번)
  
  myServo.attach(9);
  
  pinMode(mosfetA,OUTPUT);
  digitalWrite(mosfetA,HIGH);

  // 시리얼 통신 시작
  Serial.begin(115200);
  
  // 사용자에게 안내 메시지 출력
  Serial.println("Enter pulse width in microseconds (1000 - 2000):");
}

void loop() {
  // 시리얼 입력이 있을 경우 처리
  if (Serial.available() > 0) {
    // 입력된 데이터를 문자열로 읽기
    String input = Serial.readStringUntil('\n');
    
    // 입력된 데이터를 숫자로 변환
    int pulseWidth = input.toInt();

    // 마이크로초 단위의 입력이 유효한 범위 내에 있는지 확인 (보통 1000 ~ 2000)
    if (pulseWidth >= 400 && pulseWidth <= 2600) {
      // 서보 모터에 해당 펄스 폭 적용
      myServo.writeMicroseconds(pulseWidth);
      Serial.print("Pulse width set to: ");
      Serial.println(pulseWidth);
    } else {
      // 유효하지 않은 입력일 경우 에러 메시지 출력
      Serial.println("Invalid input. Please enter a value between 1000 and 2000.");
    }
  }

  //else  Serial.println(analogRead(currentA));
}
