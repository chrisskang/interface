
// ------------------------------------------------------
// DATA Package Handler
// ------------------------------------------------------


void setHandler(uint8_t id, char header, String data) {
  // Placeholder for handling special IDs
  if(monitoring) Serial.println("Special ID detected.");
}

void unitHandler(int setIndex, char header, String data) {
  switch (header) {
    case 'S':
      // Handle full sensor read
      if(monitoring) Serial.println("Full sensor read.");
      break;
    case 'P':
      // Handle PWM read
      if(monitoring) Serial.println("PWM read.");
      //sendPWMData(unitID[setIndex]);
      break;
    case 'R':
      // Handle EEROM read
      if(monitoring) Serial.println("EEROM read.");
      break;
    case 'A':
      // Save EEROM - AS5600 Origin Position
      if(monitoring) Serial.println("Save EEROM - AS5600 Origin Position.");
      break;
    case 'C':
      // Save EEROM - Current Threshold
      if(monitoring) Serial.println("Save EEROM - Current Threshold.");
      break;
    case 'T':
      // Save EEROM - Max Network LOSS
      if(monitoring) Serial.println("Save EEROM - Max Network LOSS.");
      break;
    case 'M':
      // Mosfet Write
      if(monitoring) Serial.println("Mosfet Write.");
      break;
    case 'V':
      // Servo PWM Write
      if(monitoring) Serial.println("Servo PWM Write.");
      break;
    case 'L':
      // LED PWM Write
      if(monitoring) Serial.println("LED PWM Write.");
      break;
    case 'H':
      // LED PWM Write
      if(monitoring) Serial.println("Hold");
      break;
    case 'X':
      // LED PWM Write
      if(monitoring) Serial.println("Turn Off");
      break;            
    default:
      if(monitoring) Serial.println("Unknown header.");
      break;
  }
}



// ------------------------------------------------------
// Individual Functions
// ------------------------------------------------------
