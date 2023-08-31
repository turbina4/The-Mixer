const byte numberOfPotentiometers = 3; // Enter the number of potentiometers here
const int potentiometersPins[numberOfPotentiometers] = {A0, A1, A2}; // Enter potentiometers pins here

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < numberOfPotentiometers; i++) {
    pinMode(potentiometersPins[i], INPUT);
  }
}

void loop() {
  int mapped[numberOfPotentiometers];
  for (int i = 0; i < numberOfPotentiometers; i++) {
    mapped[i] = map(analogRead(potentiometersPins[i]), 0, 1023, 0, 100);
    Serial.print(mapped[i]);
    Serial.print("/");
  }
  Serial.println();
  delay(100);
}