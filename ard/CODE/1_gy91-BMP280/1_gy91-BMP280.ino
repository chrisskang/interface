#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

// BMP280 I2C 주소 (GY-91 모듈의 BMP280은 기본 주소 0x76 또는 0x77)
#define BMP280_I2C_ADDRESS 0x76

Adafruit_BMP280 bmp;


void I2Cscan(){
  byte error, address;
  int nDevices;
  
  Serial.println("I2C 장치를 스캔하는 중입니다...");
  
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("I2C 장치가 발견되었습니다. 주소: 0x");
      if (address<16) 
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println(" !");
      
      nDevices++;
    }
    else if (error==4) {
      Serial.print("알 수 없는 에러가 발생하였습니다. 주소: 0x");
      if (address<16) 
        Serial.print("0");
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0)
    Serial.println("I2C 장치를 찾을 수 없습니다.\n");
  else
    Serial.println("스캔 완료.\n");
}



void setup() {
  Serial.begin(115200);
  while (!Serial); // 시리얼 모니터가 준비될 때까지 기다립니다.
  Wire.begin(33, 32);
  I2Cscan();

  delay(10);
  if (!bmp.begin(BMP280_I2C_ADDRESS)) {
    Serial.println("BMP280 센서를 찾을 수 없습니다. 연결을 확인하세요.");
    while (1);
  }
  
  Serial.println("BMP280 센서 초기화 완료.");
}

void loop() {
  int everage = 20;
  float pressure,temperature,altitude;
  
  for(int i=0;i<everage;i++){
    pressure += bmp.readPressure() / 100.0F;
    temperature += bmp.readTemperature();
    altitude += bmp.readAltitude(1013.25);
    delay(1);
  }

  pressure = pressure/everage;
  temperature = temperature/everage;
  altitude = altitude/everage;

  Serial.print("기압: ");
  Serial.print(pressure);
  Serial.print(" hPa, 온도: ");
  Serial.print(temperature);
  Serial.print(" C, 고도: ");
  Serial.print(altitude);
  Serial.println(" m");

  delay(500); // 1초마다 측정
}
