String starts, ends, initial, msg, check, sending;

void setup() {
  Serial.begin(9600);

  starts = String("!!!");
  ends = String("???");
  initial = String("incorrect code");
  msg = String("DATA");
  check = String("code");
}



void loop() {
  if(Serial.available() > 0) {
  //Serial.write(Serial.read());
   String str = Serial.readString();
   if (str == check) {
    sending = starts + msg + ends;
    }
    else {
     sending = starts + initial + ends;
      }
    Serial.print(sending);
    //Serial.print(str.length());
    }
}
