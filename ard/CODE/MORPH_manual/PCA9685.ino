/*  
 *  PCA9685
 *  ch0 : ServoB-Mosfet
 *  ch1 : servoB-PWM
 *  ch2 : LED-B3
 *  ch3 : LED-B2
 *  ch4 : LED-B1
 *  ch5 : LED-A3
 *  ch6 : LED-A2
 *  ch7 : LED-A1
 *  ch14 : ServoA-PWM
 *  ch15 : ServoA-Mosfet
 */

// 서보 모터의 최소 및 최대 펄스 길이를 정의합니다.
#define SERVOMIN  90   // 440 µsec
#define SERVOMAX  1385 // 2465 µsec

#define USMIN  440  // 최소 펄스 길이 (440 µsec)
#define USMAX  2465 // 최대 펄스 길이 (2465 µsec)

#define SERVO_FREQ 50 // 서보 주파수 설정 (50 Hz)
void setServoPulse(uint8_t n, int pulse) {
  double pulselength = 1000000.0 / SERVO_FREQ / 4096.0; // 1,000,000 us per second / frequency / 12 bits resolution
  int pulseval = pulse / pulselength;
  PCA9685.setPWM(1, 0, pulseval);
  PCA9685.setPWM(14, 0, pulseval);
}
