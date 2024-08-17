#include <SoftwareSerial.h>

// 소프트웨어 시리얼 객체 생성 (RX, TX 핀 지정)
SoftwareSerial mySerial(3, 5);

// RS485 제어 핀
const int controlPin = 4;

void setup() {
  // 시리얼 통신 초기화
  Serial.begin(115200);
  mySerial.begin(9600);
  
  // 제어 핀을 출력으로 설정
  pinMode(controlPin, OUTPUT);
  digitalWrite(controlPin, LOW); // 초기 상태: 수신 모드
}

void loop() {
  // 수신 모드: 데이터가 들어오는지 확인
  if (mySerial.available()) {
    digitalWrite(controlPin, LOW); // 수신 모드
    while (mySerial.available()) {
      char receivedChar = mySerial.read();
      Serial.println(receivedChar); // 수신된 문자 출력
    }
  }
  
  // 송신 모드: 사용자의 입력을 송신
  if (Serial.available()) {
    digitalWrite(controlPin, HIGH); // 송신 모드
    while (Serial.available()) {
      char dataToSend = Serial.read();
      mySerial.write(dataToSend);
    }
    delay(100); // 데이터 전송 후 잠시 대기
    digitalWrite(controlPin, LOW); // 수신 모드로 돌아가기
  }
}
