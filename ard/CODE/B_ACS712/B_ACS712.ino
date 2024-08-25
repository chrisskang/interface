#include <ACS712.h>

ACS712 sensor(ACS712_20B, A1);  // 20A model, A1 pin

void setup() {
  Serial.begin(115200);
  sensor.calibrate();  // Calibrate sensor at startup
}

void loop() {
  float current = sensor.getCurrentAC();  // Measure AC current
  Serial.print("Current: ");
  Serial.print(current);
  Serial.println(" A");
  delay(1000);
}
