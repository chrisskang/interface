#include <Wire.h>

#define TCA9548_ADDR 0x70
#define INA226_ADDR  0x77
#define AS5600_ADDR  0x36

// *  TCA9548 Channel 
// *  ch2 : INA-A
// *  ch3 : AS-A
// *  ch4 : AS-B
// *  ch5 : INA-B

uint8_t ch[2][2] = {    //INA,AS
  {2,3},
  {5,4}
};


// --------------------- AS5600 var----------------

// Magnetic sensor variables for two channels
int magnetStatus[2] = {0, 0}; // value of the status register (MD, ML, MH)
int lowbyte[2]; // raw angle 7:0
word highbyte[2]; // raw angle 7:0 and 11:8
int rawAngle[2]; // final raw angle 
float degAngle[2]; // raw angle in degrees (360/4096 * [value between 0-4095])
int quadrantNumber[2], previousquadrantNumber[2]; // quadrant IDs
float numberofTurns[2] = {0, 0}; // number of turns
float correctedAngle[2] = {0, 0}; // tared angle - based on the startup value
float startAngle[2] = {0, 0}; // starting angle
float totalAngle[2] = {0, 0}; // total absolute angular displacement
float previoustotalAngle[2] = {0, 0}; // for the display printing

// --------------------- INA226 ----------------
#include <INA226_WE.h>
INA226_WE ina226 = INA226_WE(INA226_ADDR);



// ------------------------------------------------------
// TCA Functions
// ------------------------------------------------------


void setupTCA(){
  for(int i=0;i<2;i++){
    // INA226 Setup ----------------------------------------
    selectTCAChannel(ch[i][0]);
    
    Serial.print("\tUnitID ");
    Serial.print(unitID[i]);
    Serial.print( "\t");    
    Serial.print("[INA226]");
    
    if(!ina226.init()){
      Serial.println("\t**Failed to init INA226");
      //while(1){}
    }else{
      ina226.setResistorRange(0.007,8.0);  // 100mOhm and 1.3A
      //ina226.setCorrectionFactor(1.2);   
      ina226.setAverage(AVERAGE_16);
      ina226.setConversionTime(CONV_TIME_588); //choose conversion time and uncomment for change of default
      //ina226.waitUntilConversionCompleted(); 
      connINA[i] = true;
      Serial.println(" ready");
    }

    // AS5600 Setup ----------------------------------------
    selectTCAChannel(ch[i][1]);
    Serial.print("\tUnitID ");
    Serial.print(unitID[i]);
    Serial.print( "\t");    
    Serial.print("[AS4500]");
    
      Wire.beginTransmission(AS5600_ADDR);
      if (!Wire.endTransmission()) {
        //checkMagnetPresence(i); // Check the magnet presence
        readRawAngle(i); // Make a reading to update degAngle
        startAngle[i] = degAngle[i]; // Set startAngle to degAngle for taring 
        Serial.println(" ready");
        connAS[i] = true;
      }else{
        Serial.println("\t**Failed to init AS5600");
      }
  }
}

void TCAReset(){
    digitalWrite(TCAreset,LOW);
    delay(10);
    digitalWrite(TCAreset,HIGH);
    delay(10);
}

void selectTCAChannel(uint8_t channel) {
  // Function to select a specific channel on TCA9548
  if (channel < 0 || channel > 7) {
    Serial.println("Invalid TCA9548 channel");
    return;
  }
  

  Wire.beginTransmission(TCA9548_ADDR);
  Wire.write(1 << channel);
  uint8_t error = Wire.endTransmission();
  
  if (error) {
    Serial.print("Error selecting TCA channel: ");
    Serial.println(error);
    // Handle the error, for example by retrying
    delay(100);  // Wait before retrying
    Wire.beginTransmission(TCA9548_ADDR);
    Wire.write(1 << channel);
    error = Wire.endTransmission();
    if (error) {
      Serial.print("Retry failed. Error: ");
      Serial.println(error);
    } else {
      Serial.println("Retry succeeded.");
    }
  }
}


// ------------------------------------------------------
// INA226 Functions
// ------------------------------------------------------



void readINA(int channel,boolean full){

  selectTCAChannel(ch[channel][0]);
  
  float shuntVoltage_mV = 0.0;
  float loadVoltage_V = 0.0;
  float busVoltage_V = 0.0;
  float current_mA = 0.0;

  if(full){
    shuntVoltage_mV = ina226.getShuntVoltage_mV();
    Serial.print(shuntVoltage_mV);
    Serial.print("\t");
    
    busVoltage_V = ina226.getBusVoltage_V();    
    Serial.print(busVoltage_V);
    Serial.print("\t");
    
    loadVoltage_V  = busVoltage_V + (shuntVoltage_mV/1000);
    
    sensor[channel][0] = int(loadVoltage_V*100);
  }

  current_mA = ina226.getCurrent_mA();
  sensor[channel][1] = int(current_mA*100);
  
  
  if(monitoring){
    Serial.print("[INA226] ");
    Serial.print(unitID[channel]);
    
    checkForI2cErrors();
    if(full)    Serial.print("\tLoad Voltage [V]:"); Serial.print(loadVoltage_V);
    Serial.print("\tCurrent[mA]:"); Serial.print(current_mA);
  
    if(ina226.overflow){
      Serial.print("\t**Overflow");
    }
    Serial.print("\t");
    
  }
}

void checkForI2cErrors(){
  byte errorCode = ina226.getI2cErrorCode();
  if(errorCode){
    Serial.print("I2C error:\t");
    Serial.print(errorCode);
    switch(errorCode){
      case 1:
        Serial.println("\tData too long to fit in transmit buffer");
        break;
      case 2:
        Serial.println("\tReceived NACK on transmit of address");
        break;
      case 3: 
        Serial.println("\tReceived NACK on transmit of data");
        break;
      case 4:
        Serial.println("\tOther error");
        break;
      case 5:
        Serial.println("\tTimeout");
        break;
      default: 
        Serial.println("\tCan't identify the error");
    }

  }
}


// ------------------------------------------------------
// AS5600 Functions
// ------------------------------------------------------



void readAS(int channel){
  selectTCAChannel(ch[channel][1]);
  readRawAngle(channel); // Read value from the sensor
  correctAngle(channel); // Tare the value
  //checkQuadrant(channel); // Check quadrant, rotations, and absolute angular position  
  
}

void readRawAngle(int channel) {
  // 7:0 bits
  Wire.beginTransmission(AS5600_ADDR); // connect to the sensor
  Wire.write(0x0D); // register map: Raw angle (7:0)
  Wire.endTransmission(); // end transmission
  Wire.requestFrom(AS5600_ADDR, 1); // request from the sensor
  
  while (Wire.available() == 0); // wait until it becomes available 
  lowbyte[channel] = Wire.read(); // read the data
  
  // 11:8 bits
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(0x0C); // register map: Raw angle (11:8)
  Wire.endTransmission();
  Wire.requestFrom(AS5600_ADDR, 1);
  
  while (Wire.available() == 0);  
  highbyte[channel] = Wire.read();
  
  highbyte[channel] = highbyte[channel] << 8; // shift to the correct place
  rawAngle[channel] = highbyte[channel] | lowbyte[channel];
  degAngle[channel] = rawAngle[channel] * 0.087890625; // calculate angle in degrees

  sensor[channel][2] = int(degAngle[channel]*100);
  if(monitoring){
    Serial.print("<AS5600> ");
    Serial.print(unitID[channel]);
    Serial.print("\t");
    Serial.print("Deg angle: ");
    Serial.print(degAngle[channel], 2);

  }
}

void correctAngle(int channel) {
  correctedAngle[channel] = degAngle[channel] - startAngle[channel];
  if (correctedAngle[channel] < 0) {
    correctedAngle[channel] += 360; // normalize negative angle
  }
  
  sensor[channel][3] = int(correctedAngle[channel]*100);
  if(monitoring){
    Serial.print("\tCorrected angle: ");
    Serial.println(correctedAngle[channel], 2);
  }
}

void checkQuadrant(int channel) {
  // Determine the quadrant number
  if (correctedAngle[channel] >= 0 && correctedAngle[channel] <= 90) {
    quadrantNumber[channel] = 1;
  } else if (correctedAngle[channel] > 90 && correctedAngle[channel] <= 180) {
    quadrantNumber[channel] = 2;
  } else if (correctedAngle[channel] > 180 && correctedAngle[channel] <= 270) {
    quadrantNumber[channel] = 3;
  } else if (correctedAngle[channel] > 270 && correctedAngle[channel] < 360) {
    quadrantNumber[channel] = 4;
  }

  // Check for quadrant changes and update the number of turns
  if (quadrantNumber[channel] != previousquadrantNumber[channel]) {
    if (quadrantNumber[channel] == 1 && previousquadrantNumber[channel] == 4) {
      numberofTurns[channel]++;
    } else if (quadrantNumber[channel] == 4 && previousquadrantNumber[channel] == 1) {
      numberofTurns[channel]--;
    }
    previousquadrantNumber[channel] = quadrantNumber[channel];
  }

  totalAngle[channel] = (numberofTurns[channel] * 360) + correctedAngle[channel];
  Serial.print("Channel ");
  Serial.print(channel);
  Serial.print(" - Total angle: ");
  Serial.println(totalAngle[channel], 2);
}

void checkMagnetPresence(int channel) {
  while ((magnetStatus[channel] & 32) != 32) {
    magnetStatus[channel] = 0;

    Wire.beginTransmission(AS5600_ADDR); // connect to the sensor
    Wire.write(0x0B); // register map: Status: MD ML MH
    Wire.endTransmission(); // end transmission
    Wire.requestFrom(AS5600_ADDR, 1); // request from the sensor

    while (Wire.available() == 0); 
    magnetStatus[channel] = Wire.read();
  }
}
