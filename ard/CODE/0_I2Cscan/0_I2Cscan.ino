#include <Wire.h>

void setup() {
  Serial.begin(115200);
  while (!Serial); // 시리얼 모니터가 준비될 때까지 기다립니다.
  pinMode(7,OUTPUT);
  digitalWrite(7,HIGH);
  //TWCR = 0;
  Wire.begin(); // SDA, SCL 핀 설정

  Serial.println("I2C 스캐너를 시작합니다.");
}

void loop() {
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
  
  delay(5000); // 5초마다 스캔
}


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
