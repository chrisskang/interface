#include <Wire.h>

// I2C 포트 A 설정
TwoWire I2C = TwoWire(0);
const int SDA_A = 8;
const int SCL_A = 9;

// I2C 포트 B 설정
const int SDA_B = 9;
const int SCL_B = 8;

// I2C 장치 스캔 함수
void scanI2C(TwoWire &i2c, const char* portName, int sdaPin, int sclPin) {
  Serial.printf("Scanning I2C devices on %s (SDA: %d, SCL: %d)...\n", portName, sdaPin, sclPin);
  i2c.begin(sdaPin, sclPin);
  byte count = 0;
  for (byte address = 1; address < 127; ++address) {
    i2c.beginTransmission(address);
    byte error = i2c.endTransmission();
    if (error == 0) {
      Serial.printf("Found I2C device at 0x%02X\n", address);
      count++;
    } else if (error == 4) {
      Serial.printf("Unknown error at address 0x%02X\n", address);
    }
  }
  if (count == 0) {
    Serial.println("No I2C devices found.\n");
  } else {
    Serial.printf("Found %d devices.\n\n", count);
  }
  i2c.end();
}

void setup() {
  Serial.begin(115200);
  while (!Serial); // 시리얼 포트 준비될 때까지 대기
  delay(1000); // 잠시 대기

  Serial.println("Initializing I2C ports...");

  // I2C 포트 A 스캔
  scanI2C(I2C, "I2C_A", SDA_A, SCL_A);
  // I2C 포트 B 스캔
  scanI2C(I2C, "I2C_B", SDA_B, SCL_B);
}

void loop() {
  // do nothing
}
