#include "HX711.h"
#include "string.h"  
#include "stdlib.h"
#include "stdio.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = A14;
const int LOADCELL_SCK_PIN = A15;

HX711 scale;

void setup() {
  Serial.begin(9600); //baud rate needs to match Xbee, 9600
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {
long reading = 0;
char str[40];

  if (scale.is_ready()) {
     reading = scale.read();
    Serial.print("HX711 reading: ");
    //Serial.println(reading);
  } else {
    Serial.println("HX711 not found.");
  }
  
  ultoa (reading,str,10);;
  
  Serial.println(reading);

  delay(1000);
  
}
