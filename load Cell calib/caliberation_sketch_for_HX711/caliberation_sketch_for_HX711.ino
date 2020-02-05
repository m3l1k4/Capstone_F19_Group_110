/* Calibration sketch for HX711 */
 
#include "HX711.h"  // Library needed to communicate with HX711 https://github.com/bogde/HX711
 
#define DOUT  5  // Arduino pin 6 connect to HX711 DOUT
#define CLK  4  //  Arduino pin 5 connect to HX711 CLK
 
//HX711 scale(DOUT, CLK);  // Init of library
HX711 get_units();
void setup() {
  Serial.begin(9600);
  HX711 set_scale();  // Start scale
HX711  tare();       // Reset scale to zero

}

void loop() {
  float current_weight=get_units(20);  // get average of 20 scale readings
  float scale_factor=(current_weight/0.145);  // divide the result by a known weight
  Serial.println(scale_factor);  // Print the scale factor to use
}
