void setup() {
  // put your setup code here, to run once:
 Serial.begin(115200);
  int totaltime = 0;
 for (int i = 1; i < 19; i++){

    int unitID1 = i * 2 -1;
    int unitID2 = i *2;

    //1 -> 1
    //36 -> 1
    //2 -> 2
    //35 -> 2

    unsigned long timeToWaitFirstCH = ((groupCalc(unitID1)) -1) * 10000 + 1000;
    unsigned long timeToWaitSecondCH = ((groupCalc(unitID2)) -1) * 10000 + 1000;

    Serial.print("for id: ");
    Serial.print(unitID1);
    Serial.print(" group num is:");
    Serial.print(groupCalc(unitID1));
    Serial.print(" wait for: ");
    Serial.println(timeToWaitFirstCH);

    Serial.print("for id: ");
    Serial.print(unitID2);
    Serial.print(" group num is:");
    Serial.print(groupCalc(unitID2));
    Serial.print(" wait for: ");
    Serial.println(timeToWaitSecondCH);
    delay(500);
}


  

}

void loop() {
  // put your main code here, to run repeatedly:

}
unsigned long groupCalc (int id){
    if (id <= 18){
      return id;
    }
    else{
      return (37 - id);
    }
  }
