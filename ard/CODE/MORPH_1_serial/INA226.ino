// ------------------------------
//    INA226
// ------------------------------
#include <Wire.h>
#include <INA226_WE.h>
INA226_WE ina226[] = { INA226_WE(INA_A_addr), INA226_WE(INA_B_addr) };




// ------------------------------------------------------
// INA226 Functions
// ------------------------------------------------------
void ina226_init(int ch){   
  Serial.print("\t[INA226] init.");
    if(!ina226[ch].init()){
      Serial.println("\t**Failed.");
    }else{
      ina226[ch].setResistorRange(0.007,8.0);  // 100mOhm and 1.3A
      ina226[ch].setCorrectionFactor(0.77);   
      ina226[ch].setAverage(AVERAGE_16);
      //ina226.setConversionTime(CONV_TIME_588); //choose conversion time and uncomment for change of default
      //ina226.waitUntilConversionCompleted(); 
      initINA[ch] = true;
      ina226[ch].waitUntilConversionCompleted(); 
      Serial.print("\tDone.");
    }
}



void readINA(int ch){
  
  float shuntVoltage_mV = 0.0;
  float loadVoltage_V = 0.0;
  float busVoltage_V = 0.0;
  float current_mA = 0.0;

  shuntVoltage_mV = ina226[ch].getShuntVoltage_mV();
  busVoltage_V = ina226[ch].getBusVoltage_V();        
  loadVoltage_V  = busVoltage_V + (shuntVoltage_mV/1000);
  current_mA = ina226[ch].getCurrent_mA();

  Voltage[ch] = uint8_t(loadVoltage_V*10);
  Current[ch] = uint8_t(current_mA/100);


  if(monitoring){
    Serial.print(loadVoltage_V);
    Serial.print("\tmA: ");
    Serial.print(current_mA);
    Serial.print("\t");
    Serial.print(Voltage[ch]);
    Serial.print("\t");    
    Serial.print(Current[ch]);
    Serial.print("\t");
  }
    
//  if(monitoring){
//    Serial.print("[INA226-");
//    Serial.print(unitID[ch]);
//    Serial.print("]\tV: ");
//    
//    //checkForI2cErrors();
//
//    Serial.print(loadVoltage_V);
//    Serial.print("\tmA: ");
//    Serial.print(current_mA);
//    Serial.print("\t");
//  
//    if(ina226[ch].overflow)    Serial.print("**Overflow");
//  }
}

//void checkForI2cErrors(){
//  byte errorCode = ina226.getI2cErrorCode();
//  if(errorCode){
//    Serial.print("I2C error:\t");
//    Serial.print(errorCode);
//    switch(errorCode){
//      case 1:
//        Serial.println("\tData too long to fit in transmit buffer");
//        break;
//      case 2:
//        Serial.println("\tReceived NACK on transmit of address");
//        break;
//      case 3: 
//        Serial.println("\tReceived NACK on transmit of data");
//        break;
//      case 4:
//        Serial.println("\tOther error");
//        break;
//      case 5:
//        Serial.println("\tTimeout");
//        break;
//      default: 
//        Serial.println("\tCan't identify the error");
//    }
//  }
//}
//
