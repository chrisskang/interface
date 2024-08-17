#include <Wire.h>
#include <MPU9250_asukiaaa.h>
#include <Adafruit_BMP280.h>
#include <math.h>

#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 33
#define SCL_PIN 32
#endif

Adafruit_BMP280 bme; // I2C
MPU9250_asukiaaa mySensor;
float aX, aY, aZ, gX, gY, gZ;
float roll, pitch;
float alpha = 0.98; // 보수 필터 계수

unsigned long lastTime;

void setup() {
  Serial.begin(115200);
  while (!Serial);

#ifdef _ESP32_HAL_I2C_H_ // For ESP32
  Wire.begin(SDA_PIN, SCL_PIN);
  mySensor.setWire(&Wire);
#else
  Wire.begin();
  mySensor.setWire(&Wire);
#endif

  bme.begin();
  mySensor.beginAccel();
  mySensor.beginGyro();
  mySensor.beginMag();

  // 초기 각도 설정
  roll = 0.0;
  pitch = 0.0;
  
  lastTime = millis();
}

void loop() {
  if (mySensor.accelUpdate() == 0) {
    aX = mySensor.accelX();
    aY = mySensor.accelY();
    aZ = mySensor.accelZ();
  }

  if (mySensor.gyroUpdate() == 0) {
    gX = mySensor.gyroX();
    gY = mySensor.gyroY();
    gZ = mySensor.gyroZ();
  }

  unsigned long currentTime = millis();
  float dt = (currentTime - lastTime) / 1000.0;
  lastTime = currentTime;

  // 가속도계로부터 각도 계산
  float accRoll = atan2(aY, aZ) * 180 / PI;
  float accPitch = atan2(-aX, sqrt(aY * aY + aZ * aZ)) * 180 / PI;

  // 자이로스코프 데이터 적분하여 각도 계산
  float gyroRoll = roll + gX * dt;
  float gyroPitch = pitch + gY * dt;

  // 보수 필터를 사용하여 각도 계산
  roll = alpha * gyroRoll + (1.0 - alpha) * accRoll;
  pitch = alpha * gyroPitch + (1.0 - alpha) * accPitch;

  Serial.print("Roll: ");
  Serial.print(roll);
  Serial.print(" degrees Pitch: ");
  Serial.print(pitch);
  Serial.println(" degrees");

  delay(10); // 10ms마다 데이터 출력
}
