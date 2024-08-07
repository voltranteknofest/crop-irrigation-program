#define NUM_RELAYS 4
#define SOIL_MOISTURE A3

const int relay_pins[NUM_RELAYS] = { 5, 6, 7, 8 };

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  for (int i = 0; i < NUM_RELAYS; i++) {
    pinMode(relay_pins[i], OUTPUT);
    digitalWrite(relay_pins[i], HIGH);
  }
}

void loop() {
  String signal;
  while (!Serial.available())
    ;
  signal = Serial.readString();
  signal.trim();

  if (signal.startsWith("read_moisture")) {
    int moisture_value = analogRead(SOIL_MOISTURE);
    Serial.println(moisture_value);
  }

  if (signal.startsWith("on")) {
    int relay_index = signal.substring(2).toInt();
    if (relay_index >= 0 && relay_index < NUM_RELAYS) {
      digitalWrite(relay_pins[relay_index], LOW);
      Serial.println("Acildi vana " + String(relay_index + 1));
    }
  }

  if (signal.startsWith("off")) {
    int relay_index = signal.substring(3).toInt();
    if (relay_index >= 0 && relay_index < NUM_RELAYS) {
      digitalWrite(relay_pins[relay_index], HIGH);
      Serial.println("Kapatildi vana " + String(relay_index + 1));
    }
  }
}
