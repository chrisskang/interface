#define SetID  1
const int unitID[2] = { SetID * 2 - 1, SetID * 2 };
boolean monitoring = true;

boolean connINA[2] = {false, false};
boolean connAS[2] = {false, false};
int pwm[2][4] = {{0}};
int sensor[2][4] = {{0}};

#define RXpin   3
#define TXpin   5
#define RS485EN 4
#define PCAEN   6
#define mosfetA 9
#define mosfetB 10
#define TCAreset 7

#include <Wire.h>
#include <SoftwareSerial.h>
SoftwareSerial RS485(RXpin, TXpin);

#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver PCA9685 = Adafruit_PWMServoDriver();

volatile bool dataReceived = false;
String receivedData = "";

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

  // I2C - SoftwareSerial communication settings (for MAX485)
  Serial.print("- Wire,RS485 Communication Setup");
    pinMode(TCAreset,OUTPUT);
    TCAReset();
    Wire.begin();
    //Wire.setClock(400000L); //fast clock    
    RS485.begin(115200);
    pinMode(RS485EN, OUTPUT);
    digitalWrite(RS485EN, LOW); // Receive mode
    delay(100);
  Serial.println("\t Done.");

  //TCA9548 Settings
  Serial.println("- TCA9548 Setup");
    setupTCA();
  Serial.println("- TCA9548 Setup Done.");
  
  // PCA9685 Settings
  Serial.print("- PCA9685 Setup");
    pinMode(PCAEN,OUTPUT);
    digitalWrite(PCAEN,LOW);
    PCA9685.begin(); 
    PCA9685.setOscillatorFrequency(27000000);
    PCA9685.setPWMFreq(50);
  Serial.println("- PCA9685 Setup Done.");
  
  Serial.println(" ");
  Serial.println("All READY");
  Serial.println("-----------------------------------");  


  //pinMode(13, OUTPUT);
  pinMode(mosfetA,OUTPUT);
  pinMode(mosfetB,OUTPUT);
  digitalWrite(mosfetA,LOW);
  digitalWrite(mosfetB,LOW);
  
  
}




// ------------------------------------------------------
// LOOP
// ------------------------------------------------------

void loop() {
  if (RS485.available()) {
    String received = RS485.readStringUntil('\n');
    Serial.print("Received: ");
    Serial.println(received);

    // 헥사 값으로 출력
    for (int i = 0; i < received.length(); i++) {
      Serial.print("0x");
      Serial.print(received[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
  }

//  int angle = millis() / 100;
//  angle = angle % 200;
//  Serial.println(angle);
//  if (angle > 100) {
//    digitalWrite(9, LOW);
//    digitalWrite(10, LOW);
//    delay(10);
//    PCA9685.setPWM(1, 4096, 0);
//    PCA9685.setPWM(14, 4096, 0);
//  } else {
//    digitalWrite(9, HIGH);
//    digitalWrite(10, HIGH);
//    delay(10);
//    setServoPulse(0, angle * 5 + 500);
//  }
//
//  //----------- Get Sensor
  if(connINA[0]) readINA(0,true);
  if(connAS[0])  readAS(0);  
  if(connINA[1]) readINA(1,true);
  if(connAS[1])  readAS(1);
  delay(10);
}




// ------------------------------------------------------
// DATA Package Handler
// ------------------------------------------------------


void setHandler(uint8_t id, char header, String data) {
  // Placeholder for handling special IDs
  if(monitoring) Serial.println("Special ID detected.");
}

void unitHandler(int setIndex, char header, String data) {
  switch (header) {
    case 'S':
      // Handle full sensor read
      if(monitoring) Serial.println("Full sensor read.");
      break;
    case 's':
      // Handle essential sensor read
      if(monitoring) Serial.println("Essential sensor read.");
      break;
    case 'P':
      // Handle PWM read
      if(monitoring) Serial.println("PWM read.");
      //sendPWMData(unitID[setIndex]);
      break;
    case 'R':
      // Handle EEROM read
      if(monitoring) Serial.println("EEROM read.");
      break;
    case 'A':
      // Save EEROM - AS5600 Origin Position
      if(monitoring) Serial.println("Save EEROM - AS5600 Origin Position.");
      break;
    case 'C':
      // Save EEROM - Current Threshold
      if(monitoring) Serial.println("Save EEROM - Current Threshold.");
      break;
    case 'T':
      // Save EEROM - Max Network LOSS
      if(monitoring) Serial.println("Save EEROM - Max Network LOSS.");
      break;
    case 'W':
      // PWM Full Write
      if(monitoring) Serial.println("PWM Full Write.");
      break;
    case 'M':
      // Mosfet Write
      if(monitoring) Serial.println("Mosfet Write.");
      break;
    case 'V':
      // Servo PWM Write
      if(monitoring) Serial.println("Servo PWM Write.");
      break;
    case 'L':
      // LED PWM Write
      if(monitoring) Serial.println("LED PWM Write.");
      break;
    default:
      if(monitoring) Serial.println("Unknown header.");
      break;
  }
}



// ------------------------------------------------------
// Individual Functions
// ------------------------------------------------------





void senserMonitoring(){
//  if(connINA[0]) readINA(0);
//  if(connAS[0])  readAS(0);  
//  if(connINA[1]) readINA(1);
//  if(connAS[1])  readAS(1);
//  for(int j=0;j<2;j++){  
//    for(int i=0;i<4;i++){
//      Serial.print(sensor[j][i]);
//      Serial.print("\t");
//    }
//    Serial.println();
//  }  
}



void sendSensorData(int address) {

  
  digitalWrite(RS485EN, HIGH);
  int setIndex = (address % 2 == 0) ? 1 : 0; // Determine which set to use based on address

  // get data from sensors
  if(connINA[setIndex]) readINA(setIndex,true);
  if(connAS[setIndex])  readAS(setIndex);
    
  RS485.print(address);
  RS485.print('D');
  RS485.print(' ');
  for (int i = 0; i < 4; i++) {
    RS485.print(sensor[setIndex][i]);
    RS485.print(' ');
  }
  RS485.print('\n');
  digitalWrite(RS485EN, LOW);
  Serial.println("Sensor data sent successfully.");

}

void updatePWM(int address, int values[4]) {
  int setIndex = (address % 2 == 0) ? 1 : 0; // Determine which set to use based on address
  for (int i = 0; i < 4; i++) {
    pwm[setIndex][i] = values[i];
  }
  Serial.println("PWM values updated.");
}

void sendResponse(int address, char response) {
  digitalWrite(RS485EN, HIGH);
  RS485.print(address);
  RS485.print(response);
  RS485.print('\n');
  digitalWrite(RS485EN, LOW);
  Serial.print("Response sent: ");
  Serial.println(response);
}

void sendPWMData(int address) {
  digitalWrite(RS485EN, HIGH);
  int setIndex = (address % 2 == 0) ? 1 : 0; // Determine which set to use based on address
  RS485.print(address);
  RS485.print('C');
  RS485.print(' ');
  for (int i = 0; i < 4; i++) {
    RS485.print(pwm[setIndex][i]);
    RS485.print(' ');
  }
  RS485.print('\n');
  digitalWrite(RS485EN, LOW);
  Serial.println("PWM data sent successfully.");
}
