#define servoA  9
#define servoB  10
#define ledA1   11
#define ledA2   11
#define ledA3   11
#define ledB1   6
#define ledB2   6
#define ledB3   6
      
int ledCH[2][3] = {
  {ledA1,ledA2,ledA3},
  {ledB1,ledB2,ledB3}
};

int mosfetCH[2] = {servoA,servoB};
int mosfetP[2] = {mosfetA,mosfetB};

void pwmRun(){
  
  for(int ch=0;ch<2;ch++){
    // LED
    analogWrite(ledCH[ch][0],led[ch][0]);

    // Servo
    if(mosfet[ch]==0){
      digitalWrite(mosfetP[ch],LOW);
      myServos[ch].detach();
      pinMode(mosfetCH[ch],OUTPUT);
      digitalWrite(mosfetCH[ch],LOW);
      //PCA9685.setPWM(mosfetCH[ch],4096,0);
    }else{
      digitalWrite(mosfetP[ch],HIGH);
      myServos[ch].attach(mosfetCH[ch]);
      myServos[ch].writeMicroseconds(servo[ch]);
      //setServoPulse(mosfetCH[ch],servo[ch]);
    }
  }
  
  // Servo
  
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
