// ------------------------------
//    AS5600
// ------------------------------


float startAngle1 = 0, startAngle2 = 0; // starting angles for each sensor
float correctedAngle; // tared angle - based on the startup value
int stab = 10; // wait for sensor to stabilize 


void as5600_init(int ch){
  Serial.print("\t[AS5600] init.(");
  pinMode(AS_pin[ch], OUTPUT);
  Serial.print(readRawAngle(ch));
  Serial.println(") Done.");
}



// ------------------------------------------------------
// AS5600 Functions
// ------------------------------------------------------



void readAS(int ch){

  correctAngle(ch,readRawAngle(ch));
  
}

float readRawAngle(int ch) {
  digitalWrite(AS_pin[ch], HIGH);
  delay(stab);
  
  int lowbyte; // raw angle 7:0
  word highbyte; // raw angle 7:0 and 11:8
  float degAngle; // raw angle in degrees (360/4096 * [value between 0-4095])
  int rawAngle; // final raw angle 
  
  // 7:0 bits
  Wire.beginTransmission(AS5600_addr); // connect to the sensor
  Wire.write(0x0D); // register map: Raw angle (7:0)
  Wire.endTransmission(); // end transmission
  Wire.requestFrom(AS5600_addr, 1); // request from the sensor
  
  int attempts = 0;  // 시도 횟수 초기화
  int maxAttempts = 10;  // 최대 시도 횟수

  while (Wire.available() == 0 && attempts < maxAttempts) {
      delay(50);  // 50ms 대기
      attempts++;  // 시도 횟수 증가
  }
  attempts = 0;
  lowbyte = Wire.read(); // read the data
  
  // 11:8 bits
  Wire.beginTransmission(AS5600_addr);
  Wire.write(0x0C); // register map: Raw angle (11:8)
  Wire.endTransmission();
  Wire.requestFrom(AS5600_addr, 1);
  
  while (Wire.available() == 0 && attempts < maxAttempts) {
      delay(50);  // 50ms 대기
      attempts++;  // 시도 횟수 증가
  } 
  highbyte = Wire.read();
  
  highbyte = highbyte << 8;           // shift high byte to its proper place
  rawAngle = highbyte | lowbyte;      // Combine high byte and low byte to form the raw angle
  degAngle = rawAngle * 0.087890625;  // Convert raw angle to degrees

  digitalWrite(AS_pin[ch], LOW);
  delay(1);
  return degAngle;
}

void correctAngle(int ch,float rawDeg) {
  int16_t correctedAngle;
  rawDeg = rawDeg*100; 
  correctedAngle = (int16_t)rawDeg;
  correctedAngle -= E_Origin[ch];
  Angle[ch] = correctedAngle;

  if(monitoring){
    Serial.print("CH: ");
    Serial.print(ch);
    Serial.print("\t");
    Serial.print(correctedAngle);
    Serial.print("\t");
    Serial.print(Angle[ch]);
    Serial.print("\t");
  }
}
