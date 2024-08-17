/*  
 *  ATMEGA SUPER MINI
 *  3 : 485RX
 *  4 : 485ED
 *  5 : 485TX
 *  6 : PCA-OE
 *  A5 : SCL
 *  A4 : SDA
 *  
 * 
 *  TCA9548
 *  ch2 : INA-A
 *  ch3 : AS-A
 *  ch4 : AS-B
 *  ch5 : INA-B
 *  
 *  
 *  PCA9685
 *  ch0 : ServoB-Mosfet
 *  ch1 : servoB-PWM
 *  ch2 : LED-B3
 *  ch3 : LED-B2
 *  ch4 : LED-B1
 *  ch5 : LED-A3
 *  ch6 : LED-A2
 *  ch7 : LED-A1
 *  ch14 : ServoA-PWM
 *  ch15 : ServoA-Mosfet
 */

#include <SoftwareSerial.h>

// SoftwareSerial RX, TX 핀 설정
SoftwareSerial mySerial(3, 5); // RX, TX
const int controlPin = 12; // DE 및 RE 핀

// 데이터 배열 초기화
int16_t pwm[8] = {0};     // 8개의 int16 배열
int16_t sensor[4] = {0};  // 4개의 int16 배열

void setup() {
  // 기본 시리얼 통신 설정 (USB 시리얼 모니터용)
  Serial.begin(9600);
  
  // SoftwareSerial 통신 설정 (MAX485용)
  mySerial.begin(9600);
  pinMode(controlPin, OUTPUT);
  digitalWrite(controlPin, LOW); // 수신 모드
  delay(500);

  Serial.println("RS485 Test");
  delay(500);

  pinMode(13, OUTPUT);
}

void loop() {
  if (mySerial.available()) {
    String receivedData = "";
    while (mySerial.available()) {
      char c = mySerial.read();
      receivedData += c;  // 수신된 데이터 문자열로 결합
    }
    
    Serial.println("Received: " + receivedData);
    
    // 데이터 파싱
    int address;
    char command;
    int values[8];
    int valueCount = 0;
    
    parseReceivedData(receivedData, address, command, values, valueCount);

    // address가 자신의 주소이거나 0일 때만 반응
    if (address == 0 || address == 1) { // 자신의 주소로 변경해야 합니다
      if (command == 'G') {
        sendSensorData();
      } else if (command == 'D') {
        if (valueCount == 8) {
          updatePWM(values);
          sendResponse(address, 'O');  // 데이터 수가 8개일 경우 응답
        } else {
          sendResponse(address, 'E');  // 데이터 수가 8개가 아닐 경우 오류 응답
        }
      } else if (command == 'C') {
        sendPWMData();
      }
    }
  }
}

void parseReceivedData(String data, int &address, char &command, int values[], int &valueCount) {
  int index = 0;
  address = data.substring(index, data.indexOf(' ')).toInt();
  index = data.indexOf(' ') + 1;
  command = data[index];
  index = data.indexOf(' ', index) + 1;
  
  while (index < data.length()) {
    int nextSpace = data.indexOf(' ', index);
    if (nextSpace == -1) nextSpace = data.length();
    values[valueCount++] = data.substring(index, nextSpace).toInt();
    index = nextSpace + 1;
  }
}

void sendSensorData() {
  digitalWrite(controlPin, HIGH);
  Serial.println("Sending sensor data.");
  
  mySerial.print(1);  // Address
  mySerial.print(' ');
  mySerial.print('G');  // Command
  mySerial.print(' ');

  for (int i = 0; i < 4; i++) {
    mySerial.print(sensor[i]);
    if (i < 3) {
      mySerial.print(' '); // 데이터 사이에 스페이스 추가
    }
  }
  mySerial.println(); // 줄바꿈 문자 추가
  
  digitalWrite(controlPin, LOW);
  Serial.println("Sensor data sent successfully.");
}

void updatePWM(int values[]) {
  for (int i = 0; i < 8; i++) {
    pwm[i] = values[i];
  }
}

void sendPWMData() {
  digitalWrite(controlPin, HIGH);
  Serial.println("Sending PWM data.");
  
  mySerial.print(1);  // Address
  mySerial.print(' ');
  mySerial.print('C');  // Command
  mySerial.print(' ');

  for (int i = 0; i < 8; i++) {
    mySerial.print(pwm[i]);
    if (i < 7) {
      mySerial.print(' '); // 데이터 사이에 스페이스 추가
    }
  }
  mySerial.println(); // 줄바꿈 문자 추가
  
  digitalWrite(controlPin, LOW);
  Serial.println("PWM data sent successfully.");
}

void sendResponse(int address, char response) {
  digitalWrite(controlPin, HIGH);
  Serial.println("Sending response.");

  mySerial.print(address);  // Address
  mySerial.print(' ');
  mySerial.print(response); // Response
  mySerial.println(); // 줄바꿈 문자 추가
  
  digitalWrite(controlPin, LOW);
  Serial.println("Response sent successfully.");
}
