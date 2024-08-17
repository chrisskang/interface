#include <Wire.h>


// Magnetic sensor things
int magnetStatus = 0; // value of the status register (MD, ML, MH)
int lowbyte; // raw angle 7:0
word highbyte; // raw angle 7:0 and 11:8
int rawAngle; // final raw angle 
float degAngle; // raw angle in degrees (360/4096 * [value between 0-4095])
float startAngle1 = 0, startAngle2 = 0; // starting angles for each sensor
float correctedAngle; // tared angle - based on the startup value

const int VCC1 = 7; // AS5600 module 1 VCC pin
const int VCC2 = 8; // AS5600 module 2 VCC pin

void setup() {
  Serial.begin(115200); // start serial communication
  Wire.begin(); // start I2C
  Wire.setClock(800000L); // set I2C clock speed

  pinMode(VCC1, OUTPUT);
  pinMode(VCC2, OUTPUT);

  digitalWrite(VCC1, LOW);
  digitalWrite(VCC2, LOW);

  // Initialize each sensor and store their starting angle
  startAngle1 = initSensor(VCC1);
  startAngle2 = initSensor(VCC2);
}

void loop() {    
  float angle1 = readSensor(VCC1, startAngle1);


  //Serial.print("A: \t");
  Serial.print(angle1);

  float angle2 = readSensor(VCC2, startAngle2);
  Serial.print("\t");
  Serial.println(angle2);

  //delay(10); // wait for 1 second
}

float initSensor(int vccPin) {
  digitalWrite(vccPin, HIGH); // turn on sensor
  delay(10); // wait for sensor to stabilize
  ReadRawAngle(); // read the initial angle
  float startAngle = degAngle; // store the initial angle
  digitalWrite(vccPin, LOW); // turn off sensor
  return startAngle;
}

float readSensor(int vccPin, float startAngle) {
  digitalWrite(vccPin, HIGH); // turn on sensor
  delay(10); // wait for sensor to stabilize
  ReadRawAngle(); // read the raw angle
  digitalWrite(vccPin, LOW); // turn off sensor

  // Correct the angle based on the initial reading
  correctedAngle = degAngle - startAngle;
  if (correctedAngle < 0) {
    correctedAngle += 360; // normalize the angle
  }
  return correctedAngle;
}

void ReadRawAngle() {
  // Read the low byte
  Wire.beginTransmission(0x36);
  Wire.write(0x0D);
  Wire.endTransmission();
  Wire.requestFrom(0x36, 1);
  while (Wire.available() == 0);
  lowbyte = Wire.read();

  // Read the high byte
  Wire.beginTransmission(0x36);
  Wire.write(0x0C);
  Wire.endTransmission();
  Wire.requestFrom(0x36, 1);
  while (Wire.available() == 0);
  highbyte = Wire.read();
  highbyte = highbyte << 8; // shift high byte to its proper place

  // Combine high byte and low byte to form the raw angle
  rawAngle = highbyte | lowbyte;

  // Convert raw angle to degrees
  degAngle = rawAngle * 0.087890625;

//  Serial.print("Deg angle: ");
//  Serial.print(degAngle, 2);
//  Serial.print("\t");
}
