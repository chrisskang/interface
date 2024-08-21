/***************************************************************************
* Example sketch for the INA226_WE library
*
* This sketch shows how to use the INA226 module in continuous mode with
* hardware I2C, and communicate with a slave Arduino using SoftWire.
*  
* Further information can be found on:
* https://wolles-elektronikkiste.de/ina226 (German)
* https://wolles-elektronikkiste.de/en/ina226-current-and-power-sensor (English)
* 
***************************************************************************/
#include <Wire.h>
#include <INA226_WE.h>

#define I2C_ADDRESS 0x55



// Create INA226_WE instance using hardware Wire
INA226_WE ina226(I2C_ADDRESS);

void setup() {
  Serial.begin(115200);
  
  // Initialize hardware I2C (Wire) and SoftWire (for slave communication)
  Wire.begin();

  
  if (!ina226.init()) {
    Serial.println("Failed to init INA226. Check your wiring.");
    while (1) {}
  }

  Serial.println("INA226 Current Sensor Example Sketch - Continuous");
  
  // Wait for the first conversion to complete
  ina226.waitUntilConversionCompleted();
}

void loop() {
  float shuntVoltage_mV = 0.0;
  float loadVoltage_V = 0.0;
  float busVoltage_V = 0.0;
  float current_mA = 0.0;
  float power_mW = 0.0; 

  // Read sensor data from INA226 using hardware I2C
  shuntVoltage_mV = ina226.getShuntVoltage_mV();
  busVoltage_V = ina226.getBusVoltage_V();
  current_mA = ina226.getCurrent_mA();
  power_mW = ina226.getBusPower();
  loadVoltage_V  = busVoltage_V + (shuntVoltage_mV / 1000);
  
  // Print sensor data
  Serial.print("Shunt Voltage [mV]: "); Serial.println(shuntVoltage_mV);
  Serial.print("Bus Voltage [V]: "); Serial.println(busVoltage_V);
  Serial.print("Load Voltage [V]: "); Serial.println(loadVoltage_V);
  Serial.print("Current [mA]: "); Serial.println(current_mA);
  Serial.print("Bus Power [mW]: "); Serial.println(power_mW);
  


  // Check for overflow
  if (!ina226.overflow) {
    Serial.println("Values OK - no overflow");
  } else {
    Serial.println("Overflow! Choose higher current range");
  }
  
  Serial.println();
  delay(3000);
}
