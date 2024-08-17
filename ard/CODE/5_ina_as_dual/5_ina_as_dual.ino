#include <Wire.h>

#include <INA226_WE.h>
#define mosfetA 9
#define mosfetB 10
#define I2C_ADDRESS1 0x44
#define I2C_ADDRESS2 0x45

// Create INA226_WE instances for each sensor
INA226_WE ina226_1(I2C_ADDRESS1);
INA226_WE ina226_2(I2C_ADDRESS2)

;
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

  pinMode(mosfetA,OUTPUT);
  pinMode(mosfetB,OUTPUT);
  digitalWrite(mosfetA,LOW);
  digitalWrite(mosfetB,LOW);


  // Initialize first INA226 sensor
  if (!ina226_1.init()) {
    Serial.println("Failed to init INA226 sensor 1. Check your wiring.");
    while (1) {}
  }
  
  // Initialize second INA226 sensor
  if (!ina226_2.init()) {
    Serial.println("Failed to init INA226 sensor 2. Check your wiring.");
    while (1) {}
  }

  Serial.println("INA226 Current Sensor Example Sketch - Continuous");

  // Wait for the first conversion to complete for both sensors
  ina226_1.waitUntilConversionCompleted();
  ina226_2.waitUntilConversionCompleted();


  pinMode(VCC1, OUTPUT);
  pinMode(VCC2, OUTPUT);

  digitalWrite(VCC1, LOW);
  digitalWrite(VCC2, LOW);

  // Initialize each sensor and store their starting angle
  startAngle1 = initSensor(VCC1);
  startAngle2 = initSensor(VCC2);
}

void loop() {    


    readAndPrintSensorData(ina226_1, "Sensor 1");
  readAndPrintSensorData(ina226_2, "Sensor 2");
  
  float angle1 = readSensor(VCC1, startAngle1);


  //Serial.print("A: \t");
  Serial.print(angle1);

  float angle2 = readSensor(VCC2, startAngle2);
  Serial.print("\t");
  Serial.println(angle2);

  //delay(10); // wait for 1 second
}




void readAndPrintSensorData(INA226_WE &sensor, const char* sensorName) {
  float shuntVoltage_mV = sensor.getShuntVoltage_mV();
  float busVoltage_V = sensor.getBusVoltage_V();
  float current_mA = sensor.getCurrent_mA();
  float power_mW = sensor.getBusPower();
  float loadVoltage_V = busVoltage_V + (shuntVoltage_mV / 1000);

  // Print sensor data
//  Serial.print(sensorName); Serial.print(" - Shunt Voltage [mV]: "); Serial.println(shuntVoltage_mV);
//  Serial.print(sensorName); Serial.print(" - Bus Voltage [V]: "); Serial.println(busVoltage_V);
//  Serial.print(sensorName); Serial.print(" - Load Voltage [V]: "); Serial.println(loadVoltage_V);
  //Serial.print(sensorName); Serial.print(" - Current [mA]: "); Serial.println(current_mA);
  Serial.print(busVoltage_V);
    Serial.print("\t");
//  Serial.print(sensorName); Serial.print(" - Bus Power [mW]: "); Serial.println(power_mW);
//
//  // Check for overflow
//  if (!sensor.overflow) {
//    Serial.print(sensorName); Serial.println(" - Values OK - no overflow");
//  } else {
//    Serial.print(sensorName); Serial.println(" - Overflow! Choose higher current range");
//  }
//
//  Serial.println();
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
