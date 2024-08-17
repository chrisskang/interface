#include <Wire.h>
#include <INA226_WE.h>

#define I2C_ADDRESS1 0x44
#define I2C_ADDRESS2 0x45

// Create INA226_WE instances for each sensor
INA226_WE ina226_1(I2C_ADDRESS1);
INA226_WE ina226_2(I2C_ADDRESS2);

void setup() {
  Serial.begin(115200);
  
  // Initialize hardware I2C (Wire)
  Wire.begin();

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
}

void loop() {
  readAndPrintSensorData(ina226_1, "Sensor 1");
  delay(1000);
  readAndPrintSensorData(ina226_2, "Sensor 2");
  delay(1000);
}

void readAndPrintSensorData(INA226_WE &sensor, const char* sensorName) {
  float shuntVoltage_mV = sensor.getShuntVoltage_mV();
  float busVoltage_V = sensor.getBusVoltage_V();
  float current_mA = sensor.getCurrent_mA();
  float power_mW = sensor.getBusPower();
  float loadVoltage_V = busVoltage_V + (shuntVoltage_mV / 1000);

  // Print sensor data
  Serial.print(sensorName); Serial.print(" - Shunt Voltage [mV]: "); Serial.println(shuntVoltage_mV);
  Serial.print(sensorName); Serial.print(" - Bus Voltage [V]: "); Serial.println(busVoltage_V);
  Serial.print(sensorName); Serial.print(" - Load Voltage [V]: "); Serial.println(loadVoltage_V);
  Serial.print(sensorName); Serial.print(" - Current [mA]: "); Serial.println(current_mA);
  Serial.print(sensorName); Serial.print(" - Bus Power [mW]: "); Serial.println(power_mW);

  // Check for overflow
  if (!sensor.overflow) {
    Serial.print(sensorName); Serial.println(" - Values OK - no overflow");
  } else {
    Serial.print(sensorName); Serial.println(" - Overflow! Choose higher current range");
  }

  Serial.println();
}
