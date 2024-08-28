

void pwmRun(){
  
  for(int ch=0;ch<2;ch++){
    // LED
    if(random(10)<3){
      int a = random(5,254);
      analogWrite(ledCH[ch],a);
    }
    else     analogWrite(ledCH[ch],0);

    // Servo
    if(mosfet[ch]==0){
      digitalWrite(mosfetP[ch],LOW);
      servoM[ch].detach();
      pinMode(mosfetCH[ch],OUTPUT);
      digitalWrite(mosfetCH[ch],LOW);
      
    }else{
      servoM[ch].attach(mosfetCH[ch]);
      digitalWrite(mosfetP[ch],HIGH);
      //setServoPulse(mosfetCH[ch],servo[ch]);
      servoM[ch].writeMicroseconds(servo[ch]);
    }
  }
  
  // Servo
  
}
