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

//#define calibration_factor -7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketch
//#define zero_factor 125804 //This large value is obtained using the SparkFun_HX711_Calibration sketch

//long calibration_factor =  2050.0; //This value is obtained using the SparkFun_HX711_Calibration sketch
long zero_factor =  125804; //This large value is obtained using the SparkFun_HX711_Calibration sketch

#define LOADCELL_DOUT_PIN  A5
#define LOADCELL_SCK_PIN  A4

HX711 scale;


/* Calibration sketch for HX711 */
 
#include "HX711.h"  // Library needed to communicate with HX711 https://github.com/bogde/HX711
//#include "HX711.cpp"  


void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN,LOADCELL_SCK_PIN);
  void set_scale();  // Start scale 
  void tare();       // Reset scale to zero
  Serial.println("Begin Initialisation");// Print the scale factor to use
}
 
void loop() {
  //float get_units(20);
  float current_weight;
  current_weight = scale.get_units(10);  
  
  float scale_factor=(current_weight/204.8);  // divide the result by a known weight
  Serial.print(F("scale factor = "));// Print the scale factor to use
  Serial.println(scale_factor);
  Serial.print(F("current weight = "));
  Serial.println(current_weight);
  delay(3000);
}
