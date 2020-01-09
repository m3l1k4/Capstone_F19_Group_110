// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(53, OUTPUT);
   Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(53, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(53, LOW);    // turn the LED off by making the voltage LOW
    int sensorValue = analogRead(A5);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue* (5.0 / 1023.0);
  // print out the value you read:
  Serial.println(voltage, 4);
  delay(1000);                       // wait for a second
}
