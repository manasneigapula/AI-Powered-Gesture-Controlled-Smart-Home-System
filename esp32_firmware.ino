/*
 * AI-Powered Gesture Controlled Smart Home System
 * ESP32 Firmware
 * 
 * Authors: Manas Krishna Neigapula (24BEC10104)
 *          Priyam Prakash (24BEC10139)
 * Guide:   Prof. S.P. Manikandan
 * Institution: VIT Bhopal University
 * 
 * Description:
 * Receives serial commands from Python gesture recognition script
 * and controls LED brightness via PWM on GPIO 25 and GPIO 26.
 * 
 * Command Format: LED_NUMBER:BRIGHTNESS
 * Examples:
 *   1:255  → Red LED full brightness
 *   1:128  → Red LED half brightness
 *   3:255  → Green LED full brightness
 *   0:0    → All LEDs OFF
 */

#include <Arduino.h>

// ── Pin Definitions ──────────────────────────────────────────────────────────
#define RED_LED_PIN   25    // Living Room LED (GPIO 25)
#define GREEN_LED_PIN 26    // Bedroom LED (GPIO 26)

void setup() {
  // Initialize serial communication at 115200 baud
  Serial.begin(115200);

  // Configure LED pins as PWM output
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);

  // Turn off both LEDs at startup
  analogWrite(RED_LED_PIN, 0);
  analogWrite(GREEN_LED_PIN, 0);

  // Signal ready
  Serial.println("ESP32 Ready");
  Serial.println("Waiting for gesture commands...");
}

void loop() {
  // Check if a command has arrived over serial
  if (Serial.available() > 0) {
    
    // Read command until newline
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse command format: LED_NUMBER:BRIGHTNESS
    int colonIndex = command.indexOf(':');
    
    if (colonIndex != -1) {
      int ledNum    = command.substring(0, colonIndex).toInt();
      int brightness = command.substring(colonIndex + 1).toInt();

      // Clamp brightness to valid range 0-255
      brightness = constrain(brightness, 0, 255);

      // Turn off both LEDs first
      analogWrite(RED_LED_PIN, 0);
      analogWrite(GREEN_LED_PIN, 0);

      // Execute command
      if (ledNum == 0) {
        // All OFF - already done above
        Serial.println("CMD: All LEDs OFF");
      }
      else if (ledNum == 1) {
        // Red LED (Living Room)
        analogWrite(RED_LED_PIN, brightness);
        Serial.print("CMD: Red LED brightness = ");
        Serial.println(brightness);
      }
      else if (ledNum == 3) {
        // Green LED (Bedroom)
        analogWrite(GREEN_LED_PIN, brightness);
        Serial.print("CMD: Green LED brightness = ");
        Serial.println(brightness);
      }

      // Send acknowledgment back to Python
      Serial.println("OK:" + command);
    }
  }
}
