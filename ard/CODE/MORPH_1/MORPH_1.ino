// ------------------------------
//    ID init
// ------------------------------
#define SetID  1
const int unitID[2] = { SetID * 2 - 1, SetID * 2 };
boolean monitoring = true;
bool debug = true;
bool AS = false;
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
uint8_t AS_pin[] = {AS_A,AS_B};
boolean initINA[2] = {false, false};
boolean initAS[2] = {false, false};

uint8_t mosfet[2] = {0,0};
int16_t servo[2] = {0,0};
uint8_t led[2][3] = {{0}};

uint8_t Voltage[2] = {0,0};
uint8_t Current[2] = {0,0};
int16_t Angle[2] = {0,0};


int16_t E_Origin[2] = {0,0};       // angle*100, +-18000
uint16_t E_Pulse[2] = {0,0};
uint8_t E_Current = 80;            // mA*10, max 255 = 25.5A. ex) 80 = 8A
uint8_t E_Timeout = 100;           // millis()/100, max 256 = 25.6 sec

#define USMIN  500 
#define USMAX  2400 

String feedback = "";

// ------------------------------
//    RS485 
// ------------------------------
#include <Wire.h>
#include <SoftwareSerial.h>
SoftwareSerial RS485(RXpin, TXpin);
volatile bool dataReceived = false;
String receivedData = "";

#define BUFFER_SIZE 50
uint8_t buffer[BUFFER_SIZE];
int bufferIndex = 0;

uint8_t rxBuffer[BUFFER_SIZE];  // 수신을 위한 버퍼
int rxBufferIndex = 0;          // 수신 버퍼 인덱스
// ------------------------------
//    PCA9548 
// ------------------------------
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver PCA9685 = Adafruit_PWMServoDriver();
// Set 3: 0x4F


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
  pinMode(mosfetA,OUTPUT);
  pinMode(mosfetB,OUTPUT);
  digitalWrite(mosfetA,LOW);
  digitalWrite(mosfetB,LOW);  

  // EEROM setting
  Serial.print("- EEROM init");
    EEPROM_init();
  Serial.println("\tDone.");

  // UART - SoftwareSerial communication settings (for MAX485)
  Serial.print("- RS485 Communication Setup");  
    RS485.begin(9600);
    pinMode(RS485EN, OUTPUT);
    digitalWrite(RS485EN, LOW); // Receive mode
    delay(100);
  Serial.println("\t Done.");

  // I2C - Sensors communication settings (INA226, AS5600, GY91)
  Serial.println("- I2C Communication Setup"); 
    Wire.begin();
    Wire.setClock(800000L);  
    for(int i=0;i<2;i++){
      Serial.print("\tUnitID ");
      Serial.print(unitID[i]);
      ina226_init(i);
      as5600_init(i);  
    }
  Serial.println("- I2C Communication Done");   

  // PCA9685 Settings
  Serial.print("- PCA9685 Setup");
    pinMode(PCAEN,OUTPUT);
    digitalWrite(PCAEN,LOW);
    PCA9685.begin(); 
    PCA9685.setOscillatorFrequency(27000000);
    PCA9685.setPWMFreq(50);
  Serial.println("\tDone.");


  if(monitoring){
    Serial.println("*** Test Sensor Read ***");
      readINA(0);
      readAS(0);
      readINA(1);
      readAS(1);
    for(int i=0;i<2;i++){
      Serial.print("\t[Unit ");
      Serial.print(unitID[i]);      
      Serial.print("]\tV: ");
      Serial.print(Voltage[i]);
      Serial.print("\tC: ");
      Serial.print(Current[i]);
      Serial.print("\tA: ");
      Serial.println(Angle[i]);
    }    
  }

  
  Serial.println(" ");
  Serial.println("All READY");
  Serial.println("-----------------------------------");  



  
}




// ------------------------------------------------------
// LOOP
// ------------------------------------------------------

// RS485 데이터 패킷을 처리하는 메인 함수
void loop() {
  if (RS485.available()) {
    // 수신 버퍼를 초기화하고 데이터를 읽습니다.
    rxBufferIndex = 0;
    while (RS485.available() && rxBufferIndex < BUFFER_SIZE) {
      rxBuffer[rxBufferIndex++] = RS485.read();
    }

   // 받은 데이터 전체를 1바이트 단위로 16진수 출력
    Serial.print("Received buffer: ");
    for (int i = 0; i < rxBufferIndex; i++) {
      Serial.print(rxBuffer[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    // 받은 ID 확인
    uint8_t id = rxBuffer[0];
    int ch = 0;

    if (id == unitID[0] || id == unitID[1] || id == 0) {
      if (id == unitID[1]) ch = 1;
      RSwrite(8, id);
      
      if (monitoring) {
        Serial.print(">Received Buffer  ID: ");
        Serial.println(id);
      }

      // 수신 버퍼 내 데이터를 하나씩 처리합니다.
      int i = 1;  // 첫 번째 바이트는 이미 ID이므로 건너뜁니다.
      while (i < rxBufferIndex) {
        uint8_t header = rxBuffer[i++];

        if (header == '\n' || header == ' ') {
          continue;
        }

        if (monitoring) {
          Serial.print(header, HEX);
          Serial.print(" Header: ");
          Serial.println(header);
        }

        switch (header) {
          // --------------------------READ
          case 'S': {
            RSwrite(header);

            RSwrite(8, Voltage[ch]);
            RSwrite(8, Current[ch]);


            RSwrite(16, Angle[ch]);

            break;
          }
          case 'P': {
            RSwrite(header);
            RSwrite(8, mosfet[ch]);
            RSwrite(16, servo[ch]);
            RSwrite(8, led[ch][0]);
            RSwrite(8, led[ch][1]);
            RSwrite(8, led[ch][2]);
            break;
          }
          case 'R': {
            RSwrite(header);
            RSwrite(16,readE_origin(ch));
            RSwrite(16,readE_pulse(ch));
            RSwrite(8, readE_current());
            RSwrite(8, readE_timeout());
            break;
          }

          // --------------------------WRITE : EEPROM
          case 'A': {
            uint16_t rawValue = rxBuffer[i++] | (rxBuffer[i++] << 8);
            int16_t value = (int16_t)rawValue;

            if (monitoring) {
              Serial.print(" | Value: ");
              Serial.println(value);
            }

            E_Origin[ch] = value;
            RSwrite(header);
            RSwrite(8, updateE_origin(ch) ? 1 : 0);
            break;
          }
          case 'U': {
            uint16_t value = rxBuffer[i++] | (rxBuffer[i++] << 8);
            //int16_t value = (int16_t)rawValue;

            //if (monitoring) {
              Serial.print(" | Value: ");
              Serial.println(value);
            //}

            E_Pulse[ch] = value;
            RSwrite(header);
            RSwrite(8, updateE_pulse(ch) ? 1 : 0);
            break;
          }          
          case 'C': {
            uint8_t value = rxBuffer[i++];
            if (monitoring) {
              Serial.print(" | Value: ");
              Serial.println(value);
            }

            E_Current = value;
            RSwrite(header);
            RSwrite(8, updateE_current() ? 1 : 0);
            break;
          }
          case 'T': {
            uint8_t value = rxBuffer[i++];
            if (monitoring) {
              Serial.print(" | Value: ");
              Serial.println(value);
            }

            E_Timeout = value;
            RSwrite(header);
            RSwrite(8, updateE_timeout() ? 1 : 0);
            break;
          }

          // --------------------------WRITE
          case 'M': {
            uint8_t value = rxBuffer[i++];
            mosfet[ch] = value;
            RSwrite(header);
            break;
          }
          case 'V': {
            int16_t value = rxBuffer[i++] | (rxBuffer[i++] << 8);
            if(monitoring){
              Serial.println(value);
              Serial.println(E_Pulse[ch]);
              //Serial.println(value);
              
            }
            servo[ch] = value+E_Pulse[ch];
            if(servo[ch] < USMIN) {
              servo[ch] = USMIN;
            } else if (servo[ch]> USMAX) {
              servo[ch] = USMAX;
            }
            RSwrite(header);
            break;
          }
          case 'L': {
            RSwrite(header);
            for (int j = 0; j < 3; j++) {
              led[ch][j] = rxBuffer[i++];
            }
            break;
          }
          // --------------------------BroadCast
          case 'H': {
            break;
          }
          case 'X': {
            for (int j = 0; j < 2; j++) {
              mosfet[j] = 0;
              servo[j] = 0;
              for (int k = 0; k < 3; k++) {
                led[j][k] = 0;
              }
            }
            break;
          }
          default: {
            Serial.println("   Unknown header received.");
            break;
          }
        }
      }

      // 모든 데이터를 처리한 후, endBuffer 함수 호출
      endBuffer();
    } else {
      Serial.println("ID not in unitID[0] or unitID[1]. Ignoring.");
    }
  }

  // RUN
  pwmRun();
  if(AS){
    readAS(0);
    readAS(1);
  }
  readINA(0);
  readINA(1);
  if(debug)  Serial.println("");
}



void endBuffer() {
  //Serial.println("Buffer processing completed.");
  sendBuffer();
  
}


// ------------------------------------------------------
// RS485 Functions
// ------------------------------------------------------


void sendBuffer() {
  
  if(monitoring){
    Serial.print("<< Feedback Sent:  ");
    for (int i = 0; i < bufferIndex; i++) {
      Serial.print("0x");
      Serial.print(buffer[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
  }
  
  if (bufferIndex > 0) {
    digitalWrite(RS485EN, HIGH);
    RS485.write(buffer, bufferIndex);  // 버퍼의 모든 데이터를 전송
    RS485.write(0x99);
    RS485.write(0x88);
    RS485.write(0xFF);
    digitalWrite(RS485EN, LOW);
    bufferIndex = 0;  // 버퍼 인덱스를 초기화
  }
}

void RSwrite(int type, int value) {

  if (type == 8) {
    // uint8_t 값을 버퍼에 추가
    if (bufferIndex < BUFFER_SIZE) {
      buffer[bufferIndex++] = (uint8_t)value;
    }
  } 
  else if (type == 16) {
    // uint16_t 값을 버퍼에 추가 (리틀 엔디언 형식으로)
    if (bufferIndex + 1 < BUFFER_SIZE) {
      buffer[bufferIndex++] = (uint8_t)(value & 0xFF);      // 하위 바이트 추가
      buffer[bufferIndex++] = (uint8_t)((value >> 8) & 0xFF); // 상위 바이트 추가
    }
  } 
  else {
    // 잘못된 type 값 처리 (선택 사항)
    Serial.println("Error: Unsupported type.");
  }
}

void RSwrite(char value) {

  // char 값을 버퍼에 추가
  if (bufferIndex < BUFFER_SIZE) {
    buffer[bufferIndex++] = (uint8_t)value;
  }
}
