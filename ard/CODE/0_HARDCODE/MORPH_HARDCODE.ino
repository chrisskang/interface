// ------------------------------
//    ID init
// ------------------------------
#define SetID  4
uint8_t unitID[2] = { SetID * 2 - 1, SetID * 2 };
boolean monitoring = true;
bool debug = false;
bool AS = true;
bool INA = true;

// ------------------------------
//    Pinmap
// ------------------------------
#define RXpin   3
#define TXpin   5
#define RS485EN 4
#define PCAEN   6
#define AS_A    7
#define AS_B    8
#define mosfetA 9
#define mosfetB 10


// ------------------------------
//    I2C Addr.
// ------------------------------
#define INA_A_addr   0x44
#define INA_B_addr   0x45
#define AS5600_addr  0x36
//#define PCA9685  0x40
//#define GY91


// ------------------------------
//    Container
// ------------------------------
uint8_t INA_addr[] = {INA_A_addr, INA_B_addr};
uint8_t AS_pin[] = {AS_A, AS_B};
boolean initINA[2] = {false, false};
boolean initAS[2] = {false, false};

uint8_t mosfet[2] = {0, 0};
int16_t servo[2] = {0, 0};
uint8_t led[2][3] = {{0}};

uint8_t Voltage[2] = {0, 0};
uint8_t Current[2] = {0, 0};
int16_t Angle[2] = {0, 0};


int16_t E_Origin[2] = {0, 0};      // angle*100, +-18000
uint16_t E_Pulse[2] = {0, 0};
uint8_t E_Current = 80;            // mA*10, max 255 = 25.5A. ex) 80 = 8A
uint8_t E_Timeout = 100;           // millis()/100, max 256 = 25.6 sec

#define USMIN  500
#define USMAX  2400

String feedback = "";


// ------------------------------
//    PCA9548
// ------------------------------
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver PCA9685 = Adafruit_PWMServoDriver();
#define servoA  14
#define servoB  1
#define ledA1   7
#define ledA2   6
#define ledA3   5
#define ledB1   4
#define ledB2   3
#define ledB3   2
      
int ledCH[2][3] = {
  {ledA1,ledA2,ledA3},
  {ledB1,ledB2,ledB3}
};

int mosfetCH[2] = {servoA,servoB};
int mosfetP[2] = {mosfetA,mosfetB};

// ------------------------------
//    (f) SETUP
// ------------------------------
void setup() {
  Serial.begin(115200);
  Serial.println("--------------MORPH MCU--------------");
  Serial.print("Set ID:\t");
  Serial.print(SetID);
  Serial.print("\tunitID:\t");
  Serial.print(unitID[0]);
  Serial.print(",");
  Serial.println(unitID[1]);
  Serial.println("");

  // Mosfet settings
  pinMode(mosfetA, OUTPUT);
  pinMode(mosfetB, OUTPUT);
  digitalWrite(mosfetA, LOW);
  digitalWrite(mosfetB, LOW);

  // EEROM setting
  Serial.print("- EEROM init");
  EEPROM_init();
  Serial.println("\tDone.");

  // I2C - Sensors communication settings (INA226, AS5600, GY91)
  Serial.println("- I2C Communication Setup");
  Wire.begin();
  Wire.setClock(800000L);
  for (int i = 0; i < 2; i++) {
    Serial.print("\tUnitID ");
    Serial.print(unitID[i]);
    if (INA) ina226_init(i);
    if (AS) as5600_init(i);
  }
  Serial.println("- I2C Communication Done");

  // PCA9685 Settings
  Serial.print("- PCA9685 Setup");
  pinMode(PCAEN, OUTPUT);
  digitalWrite(PCAEN, LOW);
  PCA9685.begin();
  PCA9685.setOscillatorFrequency(27000000);
  PCA9685.setPWMFreq(50);
  Serial.println("\tDone.");


  if (monitoring) {
    Serial.println("*** Test Sensor Read ***");

    if (INA) readINA(0);
    if (AS) readAS(0);
    if (INA) readINA(1);
    if (AS) readAS(1);
    for (int i = 0; i < 2; i++) {
      Serial.print("\t[Unit ");
      Serial.print(unitID[i]);
      if (initINA[i]) {
        readINA(i);
        Serial.print("]\tV: ");
        Serial.print(Voltage[i]);
        Serial.print("\tC: ");
        Serial.print(Current[i]);
        Serial.print("\tA: ");
      }

      if (initAS[i]) {
        readAS(i);
        Serial.println(Angle[i]);
      }
    }
  }


  Serial.println(" ");
  Serial.println("All READY");
  Serial.println("-----------------------------------");

}




// ------------------------------------------------------
// LOOP
// ------------------------------------------------------

void loop() {
  
  
  pwmRun();

  // Get sensor value 
  if (AS) {
    readAS(0);
    readAS(1);
  }
  // Get voltage sensor value
  if (INA) {
    readINA(0);
    readINA(1);
  }



}


// --- Funtions
int read_pulse(int ch){
  return servo[ch];
}

int read_origin_pulse(int ch){
  return readE_pulse[ch];
}

int read_origin_angle(int ch){
  return readE_origin[ch];
}

int read_current(int ch){
  return Current[ch];
}

bool turn_mosfet(int ch, bool ON){
  digitalWrite(mosfetP[ch],ON);
  delay(1);
  return ON == digitalRead(mosfetP[ch]);
}

int read_angle_sensor(int ch){
  return Angle[ch];
}

void write_pulse(int ch,int pulseInput){
  servo[ch] = pulseInput + E_Pulse[ch];
  if (servo[ch] < USMIN) {
    servo[ch] = USMIN;
  } else if (servo[ch] > USMAX) {
    servo[ch] = USMAX;
  }  

  
}
