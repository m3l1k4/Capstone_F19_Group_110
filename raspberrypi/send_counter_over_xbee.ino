/*
 *  27 January 2020
 *  1
 *  Sample code to send an incrementing counter through Serial communications. 
 *  For our current implementation, we are using an XBee antenna using the ZigBee communication protocol.
 */

void setup() {
  // Baud rate must match receiving Xbee - in our case, it is 9600.
  Serial.begin(9600);
}

void loop() {

  int a = 0;

  while(true){
    Serial.println(a);
    a++;    
    delay(1000);
  }
  
}
