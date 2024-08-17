#include <Wire.h>

// TCA9548A I2C 주소
#define TCA9548A_ADDR 0x70

// I2C 통신 타임아웃 설정
#define I2C_TIMEOUT 1000  // 1000ms

// TCA9548A 채널 선택 함수
void tca9548a_select(uint8_t channel) {
  if (channel > 7) return;
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

// I2C 버스를 스캔하는 함수
void i2c_scan() {
  byte error, address;
  int nDevices;

  Serial.println("I2C 스캔 시작...");

  nDevices = 0;
  for (address = 1; address < 127; address++ ) {
    unsigned long startTime = millis();

    // I2C 장치에 접근 시도
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if ((millis() - startTime) > I2C_TIMEOUT) {
      Serial.println("I2C 타임아웃 발생!");
      Wire.endTransmission();
      return;
    }

    if (error == 0) {
      Serial.print("I2C 장치 발견: 주소 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);
      Serial.println(" !");

      nDevices++;
    } else if (error == 4) {
      Serial.print("알 수 없는 에러 주소 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  if (nDevices == 0)
    Serial.println("I2C 장치를 찾을 수 없습니다.\n");
  else
    Serial.println("I2C 스캔 완료.\n");
}

void setup() {
    pinMode(7,OUTPUT);


  Wire.begin();
  //Wire.setClock(5000);
  Serial.begin(115200);

  for (uint8_t channel = 0; channel < 8; channel++) {
    Serial.print("채널 ");
    Serial.print(channel);
    Serial.println(":");
    tca9548a_select(channel);
     Serial.println(22);
    i2c_scan();
  }
}

void loop() {
  // 메인 루프에서는 아무 작업도 하지 않음
}
