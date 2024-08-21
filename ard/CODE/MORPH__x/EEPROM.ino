#include <EEPROM.h>

const int E_ORIGIN_ADDR = 0;   
const int E_CURRENT_ADDR = 4;
const int E_TIMEOUT_ADDR = 6;
const int E_PULSE_ADDR = 8;  



void EEPROM_init(){

  if(readE_timeout()== 0){
    Serial.print("\t**Set Initial Value");
    updateE_current();
    updateE_timeout();
    updateE_origin(0);
    updateE_origin(1);
    updateE_pulse(0);
    updateE_pulse(1);

    
  }else{
    Serial.print("\tGet EEPROM Value");
  
    E_Origin[0] = readE_origin(0);
    E_Origin[1] = readE_origin(1);
    E_Current = readE_current();
    E_Timeout = readE_timeout();
    E_Pulse[0] = readE_pulse(0);
    E_Pulse[1] = readE_pulse(1);    
    Serial.print("\toriginA: ");
    Serial.print(E_Origin[0]);
    Serial.print("\toriginB:");
    Serial.print(E_Origin[1]);
    Serial.print("\tpulseA: ");
    Serial.print(E_Pulse[0]);
    Serial.print("\tpulseB:");
    Serial.print(E_Pulse[1]);    
    Serial.print("\tCurrent: ");
    Serial.print(E_Current);
    Serial.print("\tTimeOut: ");
    Serial.print(E_Timeout);
  }
}


int16_t readE_origin(int ch){
  int16_t Origin;
  EEPROM.get(E_ORIGIN_ADDR+ch*2,Origin);
  return Origin;
}

uint16_t readE_pulse(int ch){
  uint16_t Origin;
  EEPROM.get(E_PULSE_ADDR+ch*2,Origin);
  return Origin;
}

uint8_t readE_current(){
  uint8_t Current;
  EEPROM.get(E_CURRENT_ADDR,Current);
  return Current;
}

uint8_t readE_timeout(){
  uint8_t Timeout;
  EEPROM.get(E_TIMEOUT_ADDR,Timeout);
  return Timeout;
}


bool updateE_origin(int ch){
  int16_t Origin;
  EEPROM.get(E_ORIGIN_ADDR+ch*2,Origin);
  Serial.println(Origin);
  Serial.println(E_Origin[ch]);
  if(Origin!=E_Origin[ch]) EEPROM.put(E_ORIGIN_ADDR+ch*2,E_Origin[ch]);
  EEPROM.get(E_ORIGIN_ADDR+ch*2,Origin);
  if(Origin==E_Origin[ch]) return true;
  else  return false;
}

bool updateE_pulse(int ch){
  uint16_t Origin;
  EEPROM.get(E_PULSE_ADDR+ch*2,Origin);
  Serial.println(Origin);
  Serial.println(E_Pulse[ch]);
  if(Origin!=E_Pulse[ch]) EEPROM.put(E_PULSE_ADDR+ch*2,E_Pulse[ch]);
  EEPROM.get(E_PULSE_ADDR+ch*2,Origin);
  if(Origin==E_Pulse[ch]) return true;
  else  return false;
}

bool updateE_current(){
  uint8_t Current;
  EEPROM.get(E_CURRENT_ADDR,Current);
  if(Current!=E_Current) EEPROM.put(E_CURRENT_ADDR,E_Current);
  EEPROM.get(E_CURRENT_ADDR,Current);
  if(Current==E_Current) return true;
  else  return false;
}

bool updateE_timeout(){
  uint8_t Timeout;
  EEPROM.get(E_TIMEOUT_ADDR,Timeout);
  if(Timeout!=E_Timeout) EEPROM.put(E_TIMEOUT_ADDR,E_Timeout);
  EEPROM.get(E_TIMEOUT_ADDR,Timeout);
  if(Timeout==E_Timeout) return true;
  else  return false;
}
