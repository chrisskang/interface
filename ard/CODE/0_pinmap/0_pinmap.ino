// Pin Map
#define servoA    2
#define servoApwm 7
#define ledA1     3
#define ledA2     4
#define ledA3     5

#define servoB    37
#define servoBpwm 35
#define ledB1     38
#define ledB2     39
#define ledB3     40

int PIN[] = {2,3,4,5,37,38,39,40};

void setup() {
  pinMode(servoA,OUTPUT);
  pinMode(servoApwm,OUTPUT);
  pinMode(ledA1,OUTPUT);
  pinMode(ledA2,OUTPUT);
  pinMode(ledA3,OUTPUT);
  
  pinMode(servoB,OUTPUT);
  pinMode(servoBpwm,OUTPUT);
  pinMode(ledB1,OUTPUT);
  pinMode(ledB2,OUTPUT);
  pinMode(ledB3,OUTPUT);

  digitalWrite(servoA,HIGH);
  digitalWrite(servoApwm,LOW);
  digitalWrite(ledA1,HIGH);
  digitalWrite(ledA2,HIGH);
  digitalWrite(ledA3,HIGH);

  digitalWrite(servoB,HIGH);
  digitalWrite(servoBpwm,LOW);
  digitalWrite(ledB1,HIGH);
  digitalWrite(ledB2,HIGH);
  digitalWrite(ledB3,HIGH);  

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
}

void loop() {

  
  Serial.println("ON");
  digitalWrite(ledA1, LOW);  
   digitalWrite(LED_BUILTIN, HIGH); 
  delay(2000);

  Serial.println("OFF");
  digitalWrite(ledA1, HIGH); 
   digitalWrite(LED_BUILTIN, LOW);
  delay(1000);   


         

}
