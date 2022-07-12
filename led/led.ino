

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define LED_PIN 6
#define LED_COUNT 4
int tick = 0;
int prev_arg = 0;
int pointer = 0;
int ticks = 0;

int LED_RED = 0;
int LED_GREEN = 255;
int LED_BLUE = 255;

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  Serial.begin(115200);     // シリアル通信を初期化する。通信速度は9600bps
}

void loop() {
  if (Serial.available() > 0){
    strip.clear();
    String data = Serial.readString();
    int brightness = data.toInt();
    for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, strip.Color(LED_RED, LED_GREEN, LED_BLUE));
    }
    strip.setBrightness(brightness);
    strip.show();
  }
}
