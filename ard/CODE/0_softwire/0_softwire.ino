#include <SoftWire.h>

SoftWire softWireA(3, 2);  // SDA: 3, SCL: 2
SoftWire softWireB(5, 4);  // SDA: 5, SCL: 4

const uint8_t AS5600_ADDR = 0x36;

// AS5600 레지스터 주소
const uint8_t AS5600_ANGLE_H = 0x0E;
const uint8_t AS5600_ANGLE_L = 0x0F;

void setup() {
  Serial.begin(115200);
  
  // SoftWire 초기화
  softWireA.begin();
  softWireB.begin();

  Serial.println("Initialization complete");
}

uint16_t readAngle(SoftWire& wire) {
  // Read high byte
  wire.beginTransmission(AS5600_ADDR);
  wire.write(AS5600_ANGLE_H);
  wire.endTransmission(false); // Use false to keep connection alive
  wire.requestFrom(AS5600_ADDR, 1);
  if (wire.available()) {
    uint8_t highByte = wire.read();
  
    // Read low byte
    wire.beginTransmission(AS5600_ADDR);
    wire.write(AS5600_ANGLE_L);
    wire.endTransmission(false); // Use false to keep connection alive
    wire.requestFrom(AS5600_ADDR, 1);
    if (wire.available()) {
      uint8_t lowByte = wire.read();
      uint16_t angle = ((highByte << 8) | lowByte) & 0x0FFF;
      return angle;
    }
  }
  return 0; // Return 0 if communication failed
}

void loop() {
  // AS5600 from port A
  uint16_t angleA = readAngle(softWireA);
  Serial.print("Angle from port A: ");
  Serial.println(angleA);
  
  // AS5600 from port B
  uint16_t angleB = readAngle(softWireB);
  Serial.print("Angle from port B: ");
  Serial.println(angleB);

  delay(1000);
}
