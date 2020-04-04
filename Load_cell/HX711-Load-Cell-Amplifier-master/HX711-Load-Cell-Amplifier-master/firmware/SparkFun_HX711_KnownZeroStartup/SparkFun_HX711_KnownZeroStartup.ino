/*
 Example using the SparkFun HX711 breakout board with a scale
 By: Nathan Seidle
 SparkFun Electronics
 Date: November 19th, 2014
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 
 Most scales require that there be no weight on the scale during power on. This sketch shows how to pre-load tare values
 so that you don't have to clear the scale between power cycles. This is good if you have something on the scale 
 all the time and need to reset the Arduino and not need to tare the scale.
 
 This example code uses bogde's excellent library: https://github.com/bogde/HX711
 bogde's library is released under a GNU GENERAL PUBLIC LICENSE
 
 The HX711 does one thing well: read load cells. The breakout board is compatible with any wheat-stone bridge
 based load cell which should allow a user to measure everything from a few grams to tens of tons.

 Arduino pin 2 -> HX711 CLK
 3 -> DOUT
 5V -> VCC
 GND -> GND
 
 The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.
 
*/

#include "HX711.h" //This library can be obtained here http://librarymanager/All#Avia_HX711

#define calibration_factor 1208.50 //This value is obtained using the SparkFun_HX711_Calibration sketch
//#define zero_factor 1500804 //This large value is obtained using the SparkFun_HX711_Calibration sketch

#define LOADCELL_DOUT_PIN  A5
#define LOADCELL_SCK_PIN  A4
long zero_factor = 0;

HX711 scale;

void setup() {
  int i=0;
  long reading = 0;


    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    Serial.begin(57000);
    Serial.println("Demo of zeroing out a scale from a known value");


    for (i = 0; i <= 1000; i++ ){
       reading = reading + scale.read();
       Serial.println (scale.read());
       Serial.print("reading ");
       Serial.print(reading);
       Serial.println();
    }
       zero_factor = reading/20;
       Serial.print("zero_factor: ");
       Serial.print(zero_factor);
       Serial.println();

  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.set_offset(zero_factor); //Zero out the scale using a previously known zero_factor

}

void loop() {
  
//Serial.print("Reading: ");
  Serial.print(scale.read()-zero_factor);
 // Serial.print(scale.get_units(), 1); //scale.get_units() returns a float
 // Serial.print(" g"); //You can change to kg but you'll need to change the calibration_factor
  Serial.println();
}
