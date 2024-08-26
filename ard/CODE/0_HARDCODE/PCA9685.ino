

void pwmRun(){
  
  for(int ch=0;ch<2;ch++){
    // LED
    for(int i=0;i<3;i++){
      PCA9685.setPWM(ledCH[ch][i],0,led[ch][i]*16);
    }

    // Servo
    if(mosfet[ch]==0){
      digitalWrite(mosfetP[ch],LOW);
      PCA9685.setPWM(mosfetCH[ch],4096,0);
    }else{
      digitalWrite(mosfetP[ch],HIGH);
      setServoPulse(mosfetCH[ch],servo[ch]);
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



// 서보 모터의 최소 및 최대 펄스 길이를 정의합니다.
#define SERVOMIN  90   // 440 µsec
#define SERVOMAX  1385 // 2465 µsec



#define SERVO_FREQ 50 // 서보 주파수 설정 (50 Hz)
void setServoPulse(uint8_t n, int pulse) {
    if (pulse < USMIN) {
    pulse = USMIN;
  } else if (pulse > USMAX) {
    pulse = USMAX;
  }
  double pulselength = 1000000.0 / SERVO_FREQ / 4096.0; // 1,000,000 us per second / frequency / 12 bits resolution
  int pulseval = pulse / pulselength;
  PCA9685.setPWM(n, 0, pulseval);
}
