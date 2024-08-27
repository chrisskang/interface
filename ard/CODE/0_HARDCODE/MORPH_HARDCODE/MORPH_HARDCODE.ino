// ------------------------------
//    ID init
// ------------------------------
#define SetID  1
uint8_t unitID[2] = { SetID * 2 - 1, SetID * 2 }; //{1,2}
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
#define MIN_PULSE_STEP 15

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
//    dataToLoopThrough    
// ------------------------------
// SEQUENCES

// 1. 0 -> motion1 -> 0 -> motion2 -> 0 -> motion3 -> 0 
// 2. 0 -> randomMotion -> 0 -> randomMotion -> 0 -> randomMotion -> 0

// 3. 0 -> motion1 -> motion2 -> motion3 -> 0
// 4. 0 -> randomMotion -> randomMotion -> randomMotion -> 0


float motion1[36];
float motion2[36];
float motion3[36];

int totalMotion = 3;


float motion1[36] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36}

float motion2[36]; = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36}

float motion3[36]; = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36}

//extract relevant data
float motion1angle[2] = {motion1[unitID[0]], motion1[unitID[1]]}
float motion2angle[2] = {motion2[unitID[0]], motion2[unitID[1]]}
float motion3angle[2] = {motion3[unitID[0]], motion3[unitID[1]]}

int HOLD_TIME = 10 //10s hold
int frameRate = 10 // 15 pulse increment * 10 per second = 150 pulse per second
int speed = 150 // 150 pulse per second
int speedAngle = speed * 4.1/50 // 12.2 angle per second

int HOLD_FRAME = HOLD_TIME * frameRate // 100 frames

//TODO reverse this back to angle per second

//get total frame per sequence
//total frame is calculated from max range of angle difference, divided by minimum pulse
//during the void loop, it always steps once

int runSequence = 1

int findMax(float arr[36]){

  int max_v = 0;
	int max_i = 0;
 
	for ( int i = 0; i < sizeof(arr)/sizeof(arr[0]); i++ )
	{
		if ( abs(array[i]) > max_v )
		{
			max_v = array[i];
			max_i = i;
		}
	}
  return max_v
}

int findMaxBetwee(float sequence[totalMotion-1][36], int start, int end){
  int max_v = 0;
  int max_i = 0;
  for ( int i = 0; i < sizeof(sequence[start])/sizeof(sequence[start][0]); i++ )
  {
    float tested_value = abs(sequence[start][i]- sequence[end][i])
    if (tested_value > max_v )
    {
      max_v = tested_value;
      max_i = i;
    }
  }
  return max_v

}

int angleToPulse(int angle){
  //angle per 50 == 4.1
  float PulsePerDegree = 50/4.1
  return int(angle * PulsePerDegree)
}

int pulseToAngle(int pulse){
  //angle per 50 == 4.1
  float DegreePerPulse = 4.1/50
  return int(angle * PulsePerDegree)
}

float seq[totalMotion][36] = {motion1angle, motion2angle, motion3angle}; //motion sequence for 1,3


int calcFrameCount(int seqNum , float sequence[totalMotion][36]){
  int frameCount = 0;
  switch (seqNum){
    case 1: //0 -> motion1 -> 0 -> motion2 -> 0 -> motion3 -> 0
    
    float sequence[totalMotion][36] = {motion1angle, motion2angle, motion3angle};
    
    for (int i = 0; i < 3; i++){
      int max = findMax(sequence[i])
      int maxStep = ceil(angleToPulse(max)/MIN_PULSE_STEP)
      frameCount += maxStep
    }
    frameCount = frameCount * 2 //double because going back to 0
    frameCount = totalMotion * HOLD_FRAME
    break

    //---------------------------
    case 2: //0 -> randomMotion -> 0 -> randomMotion -> 0 -> randomMotion -> 0
    //make sequence but randomly
    float randSequence[][3] = {}

    for (int i = 0; i < 3; i++) { //create random sequence
      int randomIndex = floor(random(0, 2.99));
      randSequence[i] = sequence[randomIndex];
    }
    calcFrameCount(1, sequence)
    break

    //---------------------------
    case 3: //0 -> motion1 -> motion2 -> motion3 -> 0
    
    //1. going into motion 1 frames
    int max = findMax(sequence[0])
    int maxStep = ceil(angleToPulse(max)/MIN_PULSE_STEP)
    frameCount += maxStep
    //2. find maximum angle difference between each motion

    for (int i = 0; i < (totalMotion-1); i++){
        int max = findMaxBetween(sequence, i, i+1)
        int maxStep = ceil(angleToPulse(max)/MIN_PULSE_STEP)
        frameCount += maxStep
    }
    frameCount = totalMotion * HOLD_FRAME

    break
    //---------------------------
    case 4: //0 -> randomMotion -> randomMotion -> randomMotion -> 0
    
    float randSequence[][3] = {}

    for (int i = 0; i < 3; i++) { //create random sequence
      int randomIndex = floor(random(0, 2.99));
      randSequence[i] = sequence[randomIndex];
    }
    calcFrameCount(3, sequence)
    break
  }
  return frameCount
}

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

  int frameCount = calcFrameCount(1, float seq[totalMotion][36])


  //CHECK ID AND CALCULATE HOW LONG TO WAIT

  unsigned long timeSince = millis(); //increment in 1.024 milliseconds
  int INIT_TIME = 10000 //10s TODO CALCULATE THIS
  int num_board_working = 14 // 36-
  int INIT_TIME_TOTAL = ((num_board_working*2)-1)* INIT_TIME + 1000 // 271000

  if (SetID < 8){
  int timeToWaitFirstCH = (unitID[0]-1) * INIT_TIME + 1000; //if set ID is 7, unitID[0] = 13, timeToWaitFirstCH = 121000
  int timeToWaitSecondCH = (unitID[1]-1) * INIT_TIME + 1000; //if set ID is 7, unitID[1] = 14, timeToWaitSecondCH = 131000
  }else{
  int timeToWaitFirstCH = (unitID[0]-9) * INIT_TIME + 1000; //if set ID is 12, unitID[0] = 23, timeToWaitFirstCH = 141000
  int timeToWaitSecondCH = (unitID[1]-9) * INIT_TIME + 1000; //if set ID is 12, unitID[1] = 24, timeToWaitSecondCH = 151000
  }


  unsigned long previousMillis = 0UL;
  unsigned long interval = 1000UL;
  //wait until timetoWaitFirstCH is reached
  if ((timeSince < timeToWaitFirstCH) && ((currentMillis - previousMillis) > interval)){
 	  println("waiting for first channel to turn on")
    previousMillis = currentMillis;
  }
  else if ((timeSince >= timeToWaitFirstCH) && (timeSince < timeToWaitSecondCH)){
    println("time to turn on first channel")
    for (int i = 0; i < 3; i++){
      if (initRoutine(0)){
        break
      }
      else{
        println("failed to initialize, attempt " + (i+1))
      }
    }
  }
  else if (timeSince >= timeToWaitSecondCH){
    println("time to turn on second channel")
    for (int i = 0; i < 3; i++){
      if (initRoutine(1)){
        break
      }
      else{
        println("failed to initialize, attempt " + (i+1))
      }
    }
  }
  else{
    println("Initialization error")
  }
  

  int currentFrame = 0;
}

boolean initRoutine(int ch){

  //1. check if angle sensor exists
  if (angleSensorExist(ch)){
    currentAngle = read_angle_sensor(ch)
  }
  else{
    currentAngle = 0
  }

  //2. translate angle to pulse
  int pulse = angleToPulse(currentAngle)

  //3. write pulse
  write_pulse(ch, pulse)

  //4. check if pulse is set correctly
  if (read_pulse(ch) == pulse){
  //5. turn on mosfet
    mosfetOn = turn_mosfet(ch, true)
  }
  else{
    println("failed to set pulse")
    return 0
  }

  //6. drive to 0
  if (mosfetOn){
  driveToSingle(ch, 0)
  }
  else{
    println("failed to turn on mosfet")
    return 0
  }
  //7. check if pulse is set correctly and angle is close to 0
  if (read_pulse(ch) == 0 && abs(read_angle_sensor(ch)) < 5){
    return 1
  }
  else{
    println("failed to drive to 0")
    return 0
  }

}

void driveToSingle(int ch, int goalPulse){

  currentPulse = read_pulse(ch);
  originPulse = read_origin_pulse(ch);

  currentPulseNormalized = currentPulse - originPulse //make it normalized to origin

  goal_range = goalPulse - currentPulseNormalized

  stepCount = ceil(goal_range / MIN_PULSE_STEP) ;


  for (int i = 0; i < stepCount; i++){
    bufferStep = i * MIN_PULSE_STEP
    if (goal_range < 0){
      bufferStep = -bufferStep
    }
    //check mosfet
    if (!digitalRead(mosfetP[ch])){
      println("failed to turn on mosfet")
      return
    }
    else{
    write_pulse(ch, currentPulseNormalized + bufferStep)
    print("Driving to: ", currentPulseNormalized + bufferStep)
    delay(100);
    }
  }

}


// ------------------------------------------------------
// LOOP
// ------------------------------------------------------

void loop() {
  println("looping")
  
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


  stepMotionLoop(1, currentFrame);

  currentFrame += 1;
    
}

int lerp(a, b, t):
    return a * (1.0 - t) + (b * t)
void stepMotionLoop(int sequenceNum, int currentFrame){

  if (checkCurrent(0) || checkCurrent(1)){ //always check current
    println("current exceeded, exiting motion looping")
  }
  else{
  

  //step minimum pulse for motion
  //psudocode

  int frameCount = 400;

  int nextFrame = 

  lin




  }
}

int checkCurrent(int ch){
  if (read_current(ch) > E_Current){
    println("current exceeded")
    return 1;
  }
  println("current is within limit")
  return 0;
}


int angleToPulse(int angle){
  //angle per 50 == 4.1
  float PulsePerDegree = 12.2
  return int(angle * PulsePerDegree)
}

bool angleSensorExist(int ch){
  if(read_angle_sensor(ch) != 0){
    return true;
  }
  return false;
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
