# Circuit Diagram — AI Gesture Smart Home

## Pin Connection Table

| Component        | Component Pin | ESP32 Pin | Via           |
|------------------|---------------|-----------|---------------|
| Red LED          | Anode (+)     | GPIO 25   | 220Ω Resistor |
| Red LED          | Cathode (−)   | GND Rail  | Direct        |
| Green LED        | Anode (+)     | GPIO 26   | 220Ω Resistor |
| Green LED        | Cathode (−)   | GND Rail  | Direct        |
| ESP32            | GND Pin       | Breadboard GND Rail | Black Jumper |
| ESP32            | USB Port      | Laptop USB | Data Cable   |

## ASCII Circuit Diagram

```
ESP32
┌─────────────────┐
│                 │
│    GPIO 25 ─────┼──── [220Ω] ──── Red LED (+) ──── Red LED (-) ──── GND
│                 │                                                      │
│    GPIO 26 ─────┼──── [220Ω] ──── Green LED (+) ── Green LED (-) ─── GND
│                 │                                                      │
│    GND ─────────┼────────────────────────────────────────────────────┘
│                 │
│    USB ─────────┼──── Laptop (Power + Serial Data)
└─────────────────┘
```

## Notes

- GPIO 25 and GPIO 26 are PWM-capable pins on the ESP32
- PWM resolution: 8-bit (0 to 255)
- PWM frequency: 5000 Hz
- 220Ω resistor limits current to ~15mA, protecting the LED
- Common GND must be shared between ESP32 and breadboard GND rail

## Serial Communication Protocol

| Command | Example | Result |
|---------|---------|--------|
| `LED:BRIGHTNESS` | `1:255` | Red LED full brightness |
| `LED:BRIGHTNESS` | `1:128` | Red LED 50% brightness |
| `LED:BRIGHTNESS` | `3:200` | Green LED 78% brightness |
| `LED:BRIGHTNESS` | `0:0`   | All LEDs OFF |

Baud Rate: **115200**
