/* Calibration sketch for HX711 */
 
#include "HX711.h"  // Library needed to communicate with HX711 https://github.com/bogde/HX711
//#include "HX711.cpp"  
#define DOUT  5  // Arduino pin 6 connect to HX711 DOUT
#define CLK  4  //  Arduino pin 5 connect to HX711 CLK
 
HX711 scale();  // Init of library

void setup() {
  Serial.begin(9600);
  //scale.begin(DOUT,CLK);
void set_scale();  // Start scale
 void tare();       // Reset scale to zero

}
 
void loop() {
float  get_units();
float current_weight;
 current_weight=get_units();  
  
  float scale_factor=(current_weight/0.145);  // divide the result by a known weight
  Serial.println(scale_factor);  // Print the scale factor to use
}
