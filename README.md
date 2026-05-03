# 🤖 AI-Powered Gesture Controlled Smart Home System

> Real-time hand gesture recognition using Google MediaPipe + ESP32 to control home devices with context-aware brightness and gesture lock/unlock system.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Platform](https://img.shields.io/badge/Platform-ESP32-red)
![Library](https://img.shields.io/badge/AI-MediaPipe-green)

---

## 📌 Project Overview

This project implements a complete gesture-controlled smart home prototype using:
- **Google MediaPipe** for real-time 21-point hand landmark detection
- **Python + OpenCV** for gesture recognition and serial communication
- **ESP32 microcontroller** for PWM-based LED brightness control

### 🌟 Two Key Innovations
1. **Context-Aware Time-Based Brightness** — Same gesture produces different brightness levels depending on time of day (Morning = 100%, Night = 20%)
2. **Gesture Lock/Unlock System** — Peace sign freezes device state to prevent accidental triggering; open palm unlocks

---

## 🛠️ Hardware Required

| Component | Qty | Cost |
|---|---|---|
| ESP32 Dev Board (38-pin) | 1 | Rs. 500 |
| Red LED (5mm) | 1 | Rs. 5 |
| Green LED (5mm) | 1 | Rs. 5 |
| 220 Ohm Resistors | 2 | Rs. 5 |
| Breadboard | 1 | Rs. 50 |
| Jumper Wires | 20 | Rs. 50 |
| Micro USB Data Cable | 1 | Included |
| Laptop with Webcam | 1 | Existing |

**Total Cost: ~Rs. 615**

---

## ⚡ Circuit Connections

| Component | ESP32 Pin | Via |
|---|---|---|
| Red LED Anode (+) | GPIO 25 | 220Ω Resistor |
| Red LED Cathode (−) | GND Rail | Direct |
| Green LED Anode (+) | GPIO 26 | 220Ω Resistor |
| Green LED Cathode (−) | GND Rail | Direct |
| ESP32 GND | Breadboard GND Rail | Black Jumper |

---

## 💻 Software Requirements

```bash
# Python Libraries
pip install opencv-python
pip install mediapipe==0.10.13
pip install pyserial
```

**Arduino IDE Setup:**
1. Add ESP32 board URL: `https://dl.espressif.com/dl/package_esp32_index.json`
2. Install **esp32 by Espressif Systems** from Board Manager
3. Select **ESP32 Dev Module**

---

## 🚀 How to Run

### Step 1 — Upload Arduino Code
- Open `esp32_firmware/esp32_firmware.ino` in Arduino IDE
- Select **Tools → Board → ESP32 Dev Module**
- Select correct COM port under **Tools → Port**
- Click **Upload**

### Step 2 — Run Python Script
```bash
# Close Arduino Serial Monitor first!
cd gesture_home
python gesture_home.py
```

---

## 🖐️ Gesture Reference

| Gesture | Fingers | Action |
|---|---|---|
| Fist | 0 | All LEDs OFF |
| One Finger | 1 | Red LED ON |
| Peace Sign | 2 | 🔒 LOCK system |
| Three Fingers | 3 | Green LED ON |
| Open Palm | 5 | 🔓 UNLOCK system |

---

## 🌅 Brightness Modes

| Mode | Key | Time | Brightness |
|---|---|---|---|
| Morning | M | 6AM - 12PM | 100% |
| Afternoon | A | 12PM - 6PM | 78% |
| Evening | E | 6PM - 10PM | 50% |
| Night | N | 10PM - 6AM | 20% |

Press **X** to return to automatic time-based mode.

---

## 📁 Project Structure

```
AI-Gesture-Smart-Home/
├── README.md
├── esp32_firmware/
│   └── esp32_firmware.ino      # Arduino code for ESP32
├── gesture_home/
│   └── gesture_home.py         # Main Python script
├── docs/
│   └── circuit_diagram.md      # Circuit connection details
└── requirements.txt            # Python dependencies
```

---

## 👨‍💻 Authors

- **Manas Krishna Neigapula**
- **Priyam Prakash** 

**Institution:** VIT Bhopal University, School of Electrical & Electronics Engineering  
**Academic Year:** 2025-2026

---

## 📄 License

This project is developed for academic purposes at VIT Bhopal University.
