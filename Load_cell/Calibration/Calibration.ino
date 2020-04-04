
#include <HX711.h>



// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = A5;
const int LOADCELL_SCK_PIN = A4;


HX711 scale;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("HX711 Calibration");
  Serial.println("Calibrating");


}

   char temp = 0;
   float num = 0;
   float weight = 0;
   float calibration_value = 0;
   
void loop() {


   
//1. Call `set_scale()` with no parameter.
  Serial.println("Set Scale:");
  scale.set_scale();     
//2. Call `tare()` with no parameter.
 // Serial.println("Tare:");
 // scale.tare();
//3. Place a known weight on the scale and call `get_units(10)`.
  Serial.println("Place known weight:");
  while ( temp != 'a' ){
    temp =  Serial.read();
  }
  Serial.println("Enter known weight:");
    weight  =  Serial.read();
  
  num = Serial.println(scale.get_units(10));
  temp = 0;
//4. Divide the result in step 3 to your known weight. You should
//   get about the parameter you need to pass to `set_scale()`  
  calibration_value = num/weight; 

  //if ( 
  Serial.println(calibration_value);
  

//delay(10000);
}
