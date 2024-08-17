#define UnitID  1

// Calculate addresses based on unit number
const int unitAddress[2] = { UnitID * 2 - 1, UnitID * 2 };
boolean connINA[2] = {false,false};
boolean connAS[2] = {false,false};

#include <Wire.h>

#include <SoftwareSerial.h>

// SoftwareSerial RX, TX pin configuration
SoftwareSerial RS485(3, 5); // RX, TX
const int RS485EN = 12; // DE and RE pin


// Split PWM and Sensor arrays into two sets
int pwm[2][4] = {{0}};    // 2 sets of 4-element int16 array
int sensor[2][4] = {{0}}; // 2 sets of 2-element int16 array

void setup() {
  // Standard serial communication settings (for USB serial monitor)
  Serial.begin(115200);
  Serial.println("");
  // I2C Communication Setting
  Wire.begin();
  Wire.setClock(800000L); //fast clock
  setupTCA();
    
  // SoftwareSerial communication settings (for MAX485)
  RS485.begin(115200);
  pinMode(RS485EN, OUTPUT);
  digitalWrite(RS485EN, LOW); // Receive mode
  delay(500);

  Serial.println(" ");
  Serial.println("All READY");
  Serial.println("-----------------------------------");  


  pinMode(13, OUTPUT);
}

void loop() {
  
  // Code to receive data
  if (RS485.available()) {
    String received = RS485.readStringUntil('\n');
    Serial.print("Received: ");
    Serial.println(received);

    // Find the first non-digit character to separate address and command
    int firstNonDigitIndex = 0;
    while (isdigit(received.charAt(firstNonDigitIndex))) {
      firstNonDigitIndex++;
    }

    // Parse address
    String addressStr = received.substring(0, firstNonDigitIndex);
    int address = addressStr.toInt();

    // Parse command
    char command = received.charAt(firstNonDigitIndex);

    // Parse values if any
    int values[4] = {0};
    int valueCount = sscanf(received.c_str() + firstNonDigitIndex + 1, "%d %d %d %d",
                            &values[0], &values[1], &values[2], &values[3]);

    // React only if the address matches unitAddress1, unitAddress2, or is 0
    if (address == unitAddress[0] || address == unitAddress[1] || address == 0) {
      // Handle commands using switch-case
      switch (command) {
        case 'G':
          sendSensorData(address);
          break;
        case 'D':
          if (valueCount == 4) {
            updatePWM(address, values);
            if (address != 0) {
              sendResponse(address, 'O');  // Response if data count is 4 and address is not 0
            }
          } else {
            if (address != 0) {
              sendResponse(address, 'E');  // Error response if data count is not 4 and address is not 0
            }
          }
          break;
        case 'C':
          sendPWMData(address);
          break;
        default:
          Serial.println("Unknown command");
          break;
      }
    }
  }


  //----------- Get Sensor



}

void sendSensorData(int address) {

  
  digitalWrite(RS485EN, HIGH);
  int setIndex = (address % 2 == 0) ? 1 : 0; // Determine which set to use based on address

  // get data from sensors
  if(connINA[setIndex]) readINA(setIndex,true);
  if(connAS[setIndex])  readAS(setIndex,true);
    
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
