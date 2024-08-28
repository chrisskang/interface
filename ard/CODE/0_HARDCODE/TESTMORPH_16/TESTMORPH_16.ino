// ------------------------------
//    ID init
// ------------------------------

//-------TOBE CHANGED-----
// SetID 16 unitID 31 XX no motor!!
#define SetID 16     
uint8_t unitID[1] = {SetID * 2 - 1}; //32, 31 but only 31
#define epulseA   1570
#define epulseB   1630

unsigned long initTotalTime = 5000;
int TIMETOZERO = 30000; //total run time to zero
long RANDOMTIME = 150000; //total run time to zero 

int ZeroSpeed = 80; //ms delay time
int randomSpeed = 80;

int goalRange = 60; //max perlin angle
#define MIN_PULSE_STEP 10 //minimum pulse step
int perlinMultiplier = 1.6; //0.01 step *3

//setid 3 gR 45
//tz = 30, rt = 60
//wait time 21000, 26000

//setid 2 gR 35
//tz = 30, rt = 60
//wait time 11000, 16000

//setid 17 gR 45
//speed 80
//tz 30 rt 150

//setid 16 gR 60
//speed 60
//tz 30 rt 150

//---------------
// bottom ids  : initTime : 
int initTime = 1000; //how long before next group starts
bool angleSensorExist[2] = {false, false}; //turn off if you want to ignore angle sensor


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
int16_t E_Pulse[2] = {0, 0};
uint8_t E_Current = 80;            // mA*10, max 255 = 25.5A. ex) 80 = 8A
uint8_t E_Timeout = 100;           // millis()/100, max 256 = 25.6 sec

#define USMIN  800
#define USMAX  2100


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



//persistence affects the degree to which the "finer" noise is seen
float persistence = 0.25;
//octaves are the number of "layers" of noise that get computed
int octaves = 3;


float x1, y1, x2, y2; 

bool initializedCH1 = false;

unsigned long timeSince = 0UL;
unsigned long startTimeLogger = 0UL;
unsigned long spentTimeLogger = 0UL;
bool measuring = false;
int dice;

bool channel1Started = false;


unsigned long startTime1 = 0;
unsigned long startMillis;

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

  // Mosfet settings
  pinMode(mosfetA, OUTPUT);
  pinMode(mosfetB, OUTPUT);
  digitalWrite(mosfetA, LOW);
  digitalWrite(mosfetB, LOW);

  // EEROM setting
  Serial.print("- EEROM init");
  EEPROM_init();
    E_Pulse[0] = epulseA;
  E_Pulse[1] = epulseB;
  Serial.println("\tDone.");

  // I2C - Sensors communication settings (INA226, AS5600, GY91)
  Serial.println("- I2C Communication Setup");
  Wire.begin();
  Wire.setClock(800000L);

  Serial.print("\tUnitID ");
  Serial.print(unitID[0]);
  if (INA) ina226_init(0);
  if (AS) as5600_init(0);
  
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

      Serial.print("\t[Unit ");
      Serial.print(unitID[0]);
      if (initINA[i]) {
        readINA(i);
        Serial.print("]\tV: ");
        Serial.print(Voltage[0]);
        Serial.print("\tC: ");
        Serial.print(Current[0]);
        Serial.print("\tA: ");
      }

      if (initAS[i]) {
        readAS(i);
        Serial.println(Angle[0]);
      }
    
  }

  Serial.println(" ");
  Serial.println("All READY");
  Serial.println("-----------------------------------");
  
  //CHECK ID AND CALCULATE HOW LONG TO WAIT
 
  long timeToWaitFirstCH = (groupCalc(unitID[0]) -1) * initTime + 1000;

  Serial.print("total init time: ");
  Serial.println(initTotalTime);


  Serial.print("for id: ");
  Serial.print(unitID[0]);
  Serial.print(" wait for: ");
  Serial.println(timeToWaitFirstCH);


  unsigned long previousMillis = 0UL;
  unsigned long interval = 1000UL;

  //wait until timetoWaitFirstCH is reached
 
  while (!(initializedCH1)){ //if not initialized
    
    timeSince = millis(); //increment in 1.024 milliseconds

  if ((timeSince - previousMillis) > interval){
 	  Serial.print("waiting for initialization ");
     Serial.print(interval);
    Serial.print("current time is : ");
    Serial.println(timeSince);
    previousMillis = timeSince;
  }
  else if ((timeSince >= timeToWaitFirstCH) && !initializedCH1){
  
    for (int i = 0; i < 3; i++){
      Serial.println("initializing first channel");
      bool initSuccess = initRoutine(0);

      if (initSuccess){
        Serial.println("initialization success");
        initializedCH1 = true;
        break;
      }
      else{
        Serial.print("failed to initialize channel 1, attempt ");
        Serial.println(i+1);
        
      }
    }

  }
  }

  delay(initTotalTime);
  
  Serial.print("EPulse0: ");
  Serial.print(E_Pulse[0]);
  Serial.print("\t EPulse1: ");
  Serial.println(E_Pulse[1]);

}

boolean initRoutine(int ch){
  int currentAngle = 0;

  //1. check if angle sensor exists // TODO ANGLE READING WRONG
  if (angleSensorExist[ch]){
    currentAngle = read_angle_sensor(ch)/100;

    Serial.print("current angle: ");
    Serial.println(currentAngle);

  }
  else{
    currentAngle = 0;
    Serial.println("angle sensor does not exist");
  }

  //2. translate angle to pulse
  int pulse = angleToPulse(currentAngle);
  

  //3. write pulse
  //write_pulse(ch, pulse);

  servo[ch] = pulse + E_Pulse[ch];
  Serial.print("current pulse is : ");
  Serial.println(read_pulse(ch));
  //Serial.println(abs(servo[ch]-newValue));
  
  
  //4. turn on mosfet
  bool mosfetOn = turn_mosfet(ch, true);
  //bool mosfetOn = true;
  Serial.println("turning on mosfet");
  delay(1000);

  //5. drive to 0
  if (mosfetOn){
    Serial.println("driving to Zero");
   
    driveToZero(ch, currentAngle, 0);
    delay(500);
    return true;
  }
  else{
    Serial.println("failed to turn on mosfet");
    delay(500);
    return false;
  }
}

void driveToZero(int ch, int currentAngle, int goalPulse){
    //goalPulse is always 0
      Serial.print("Driving from (a)");
      Serial.print(currentAngle);
      Serial.print("\t (p) ");
      Serial.print(angleToPulse(currentAngle));
      Serial.print("\t to (p)");
      Serial.println(goalPulse);

    int currentPulse = angleToPulse(currentAngle); //ie if current angle is 12 degree, pulse is +150 (angle per 50 == 4.1)

    int goal_range = goalPulse - currentPulse; //ie 0 - 150 = -150

    int stepCount = ceil(abs(goal_range / MIN_PULSE_STEP)) ; //min step is 15, stepcount is 10
    
    for (int i = 0; i < stepCount; i++){
        int bufferStep = i * MIN_PULSE_STEP; //ie 0, 15, 30, 45, 60, 75, 90, 105, 120, 135
        if (goal_range < 0){
        bufferStep = -bufferStep; //ie 0, -15, -30, -45, -60, -75, -90, -105, -120, -135
        }
        Serial.print("Movement: slowly drive To \t");
        Serial.print("currentPulse0: ");
        Serial.print(read_pulse(ch)-E_Pulse[ch] );
        Serial.print("\tnextPulse0: ");
        Serial.println(currentPulse + bufferStep);
        write_pulse(ch, (currentPulse + bufferStep)); //ie 150, 135, 120, 105, 90, 75, 60, 45, 30, 15
        
        pwmRun();
        delay(ZeroSpeed);
        if (i == (stepCount -1)){
          write_pulse(ch, 0);
          Serial.print("Driving to: ");
          Serial.println(0);
          pwmRun();
          
        }
        
    }

}

void driveToSingle(int ch, int currentAngle, int goalPulse){
    //goalPulse is always 0
      Serial.print("Driving from (a)");
      Serial.print(currentAngle);
      Serial.print("\t (p) ");
      Serial.print(angleToPulse(currentAngle));
      Serial.print("\t to (p)");
      Serial.println(goalPulse);

    int currentPulse = angleToPulse(currentAngle); //ie if current angle is 12 degree, pulse is +150 (angle per 50 == 4.1)

    int goal_range = goalPulse - currentPulse; //ie 0 - 150 = -150

    int stepCount = ceil(abs(goal_range / MIN_PULSE_STEP)) ; //min step is 15, stepcount is 10
    
    for (int i = 0; i < stepCount; i++){
        int bufferStep = i * MIN_PULSE_STEP; //ie 0, 15, 30, 45, 60, 75, 90, 105, 120, 135
        if (goal_range < 0){
        bufferStep = -bufferStep; //ie 0, -15, -30, -45, -60, -75, -90, -105, -120, -135
        }
        Serial.print("Movement: slowly drive To \t");
        Serial.print("currentPulse0: ");
        Serial.print(read_pulse(ch)-E_Pulse[ch] );
        Serial.print("\tnextPulse0: ");
        Serial.println(currentPulse + bufferStep);

        write_pulse(ch, (currentPulse + bufferStep)); //ie 150, 135, 120, 105, 90, 75, 60, 45, 30, 15
        

        pwmRun();
        delay(randomSpeed);
        
    }

}


// ------------------------------------------------------
// LOOP
// ------------------------------------------------------

void loop() {

  unsigned long currentTime = millis();
  if (currentTime < initTotalTime){
    Serial.print("current Time is : ");
    Serial.print(currentTime);
    Serial.print("\t time left is :");
    Serial.println(initTotalTime - currentTime);
    delay(1000);
  }
  else{
  //Serial.println("looping");

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
  
  //at the beginning of the sequence log time

   if (!measuring){
    // Start a new measurement cycle
    startTimeLogger = millis();
    measuring = true;
    spentTimeLogger = 0;  // Reset spentTimeLogger at the start of a new cycle
  } 
  
  if (measuring){
    // Calculate time elapsed
    spentTimeLogger = millis() - startTimeLogger;
  }

  if (spentTimeLogger < RANDOMTIME){ //
    dice = 0;
    switch(dice){
      case 0:
        movePerlin(goalRange, startMillis);
        break;

      
    }

  } else {
    // Move to zero after 5 seconds
    bool isZero = moveToZero(TIMETOZERO); //45->0 3-> 0 
    if (isZero){
      measuring = false; // Reset measuring to start a new cycle next time
      channel1Started = false;
      startMillis = millis();
    }
  }
  }
}


bool moveToZero(unsigned long maxDuration) {
  unsigned long startMillisZero = millis();  // Record the start time
  bool isAtZero = false;
  bool reachedZero = false;

  while (millis() - startMillisZero < maxDuration) {  // Run for the full duration
    unsigned long elapsedTime = millis() - startMillisZero;
    
    // Get current pulse values for both channels and adjust by E_Pulse offsets
    int currentPulse0 = read_pulse(0) - E_Pulse[0];
    //int currentPulse1 = read_pulse(1) - E_Pulse[1];

    // Flags to check if both channels have reached near-zero position
    bool channel0AtZero = abs(currentPulse0) <= 30;
    //bool channel1AtZero = abs(currentPulse1) <= 30;

    // Check if both channels are within 20 pulses of zero
    if (!reachedZero && channel0AtZero && channel1AtZero) {
      reachedZero = true;
      Serial.println("Reached zero position");
    }

    // Only adjust if we haven't reached zero yet
    if (!reachedZero) {
      // Determine next pulse values for each channel if not at zero
      int nextPulse0 = currentPulse0;
      //int nextPulse1 = currentPulse1;

      if (!channel0AtZero) {
        if (currentPulse0 < 0) {
          nextPulse0 += MIN_PULSE_STEP;
        } else {
          nextPulse0 -= MIN_PULSE_STEP;
        }
      }

        Serial.print("Movement: Zero \t");
        Serial.print("currentPulse0: ");
        Serial.print(read_pulse(0)-E_Pulse[0] );
        Serial.print("\tnextPulse0: ");
        Serial.print(nextPulse0);

      // Write the next pulse values for both channels
      write_pulse(0, nextPulse0);

      // Run the PWM for the motors
      pwmRun();
    } else {
      // New line: Indicate waiting at zero position
      Serial.print("At zero, waiting. Elapsed time: ");
      Serial.print(elapsedTime);
      Serial.println(" ms");
    }

    delay(ZeroSpeed);  // Short delay between steps
  }

  isAtZero = reachedZero;

  if (!isAtZero) {
    Serial.println("moveToZero completed without reaching zero.");
  } else {
    Serial.println("moveToZero reached and maintained zero position.");
  }

  return isAtZero;
}



void movePerlin(int gR, unsigned long startMillis){

    
    //check if both mosfet is on
    if (!(digitalRead(mosfetP[0]) )){
      Serial.println("turning on mosfet");
      turn_mosfet(0, true);
    }


    if (channel1Started == 0) startTime1 = millis();


    // Calculate time offsets
    float timeOffset1 = float(millis() - startTime1) / 10000.0f * perlinMultiplier; //0.01 -> 0.02 //

    x1 = timeOffset1;
    y1 = 10.0f; //float(unitID[0]);
 
    //PerlinNoise2 results in a float between -1 and 1
    //below we convert to a value between -goalrange and goal range
    float a1 = PerlinNoise2(x1,y1,persistence,octaves)*gR;

    int randomPulse1 = angleToPulse(a1);


    if (!channel1Started) {
        startTime1 = millis();
        driveToSingle(0, 0, randomPulse1);
        channel1Started = true;

    }

    if (channel1Started) {
        unsigned long elapsedTime = millis() - startTime1;
        Serial.print("Movement: Perlin \t");
        Serial.print("currentPulse0: ");
        Serial.print(read_pulse(0) - E_Pulse[0]);
        Serial.print("\tnextPulse0: ");
        Serial.print(randomPulse1);
        Serial.print("\t Elapsed time: ");
        Serial.print(elapsedTime);
        Serial.println(" ms");

        if (channel1Started) {
            write_pulse(0, randomPulse1);
        }
        delay(randomSpeed);
    }
    else{
      Serial.println("\t both channels are not started");
    }

}



    
//imported perlin noise functions
float PerlinNoise2(float x, float y, float persistence, int octaves)
{
    float total = 0.0;

    auto Noise2 = [](float x, float y) {
        long noise = x + y * 57;
        noise = (noise << 13) ^ noise;
        return (1.0 - (long(noise * (noise * noise * 15731L + 789221L) + 1376312589L) & 0x7fffffff) / 1073741824.0);
    };

    auto SmoothNoise2 = [&Noise2](float x, float y) {
        float corners = (Noise2(x-1, y-1) + Noise2(x+1, y-1) + Noise2(x-1, y+1) + Noise2(x+1, y+1)) / 16;
        float sides = (Noise2(x-1, y) + Noise2(x+1, y) + Noise2(x, y-1) + Noise2(x, y+1)) / 8;
        float center = Noise2(x, y) / 4;
        return (corners + sides + center);
    };

    auto CosineInterpolate = [](float a, float b, float x) {
        float ft = x * 3.1415927;
        float f = (1 - cos(ft)) * 0.5;
        return (a * (1 - f) + b * f);
    };

    auto InterpolatedNoise2 = [&](float x, float y) {
        long longX = long(x);
        float fractionX = x - longX;

        long longY = long(y);
        float fractionY = y - longY;

        float v1 = SmoothNoise2(longX, longY);
        float v2 = SmoothNoise2(longX + 1, longY);
        float v3 = SmoothNoise2(longX, longY + 1);
        float v4 = SmoothNoise2(longX + 1, longY + 1);

        float i1 = CosineInterpolate(v1, v2, fractionX);
        float i2 = CosineInterpolate(v3, v4, fractionX);

        return CosineInterpolate(i1, i2, fractionY);
    };

    for (int i = 0; i < octaves; i++)
    {
        float frequency = pow(2, i);
        float amplitude = pow(persistence, i);

        total += InterpolatedNoise2(x * frequency, y * frequency) * amplitude;
    }

    return total;
}

float lerp(float a, float b, float t){
    return a * (1.0 - t) + (b * t);
}
// ------------------------------------------------------
int checkCurrent(int ch){
  if (read_current(ch) > E_Current){
    Serial.println("current exceeded");
    return 1;
  }
  Serial.println("current is within limit");
  return 0;
}

long groupCalc (int id){
    if (id <= 18){
      return id;
    }
    else{
      return 37 - id;
    }
  }

int angleToPulse(float angle){
  //angle per 50 == 4.1
  float PulsePerDegree = 12.2;
  return int(angle * PulsePerDegree);
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
  mosfet[ch] = ON;
  return true;
//  digitalWrite(mosfetP[ch],ON);
//  delay(1);
//  return ON == digitalRead(mosfetP[ch]);
}

int read_angle_sensor(int ch){
  return Angle[ch];
}

void write_pulse(int ch,int pulseInput){
  //previously servo[ch] = pulseInput + E_Pulse[ch];
  
  if (servo[ch] == 0){
    servo[ch] = E_Pulse[ch];
  }

  int newValue = pulseInput + E_Pulse[ch];
  //Serial.println(abs(servo[ch]-newValue));

  //Serial.println(newValue);
  if( abs(servo[ch]-newValue) <= 200 ){
     servo[ch] = newValue;

  if (servo[ch] < USMIN) {
    servo[ch] = USMIN;
  } else if (servo[ch] > USMAX) {
    servo[ch] = USMAX;
  }  
  }
}
