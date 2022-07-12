

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
int brightness = 0;

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
    int current = data.toInt();
    int diff = current - brightness;
    int is_up = diff > 0;
    int sgn = 1;
    if (!is_up) {
      sgn = -1;
      diff *= -1;
    }

     for (int i = 0; i < diff; i++) {
        for (int j = 0; j < LED_COUNT; j++) {
          strip.setPixelColor(j, strip.Color(LED_RED, LED_GREEN, LED_BLUE));
        }
        strip.setBrightness(brightness + sgn * i); // Set BRIGHTNESS to about 1/5 (max = 255)
        delay(50);
        strip.show();
    }
    brightness = current;
  }
}
