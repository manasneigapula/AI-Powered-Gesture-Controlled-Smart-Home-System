# 🖐️ Gesture Control Tutorial — AI Smart Home System

> A complete beginner-friendly guide to understanding and using the gesture control system built with Google MediaPipe and ESP32.

---

## Table of Contents

1. [How Gesture Detection Works](#1-how-gesture-detection-works)
2. [Complete Gesture Reference](#2-complete-gesture-reference)
3. [Brightness Modes](#3-brightness-modes)
4. [Lock and Unlock System](#4-lock-and-unlock-system)
5. [Keyboard Controls](#5-keyboard-controls)
6. [Tips for Best Detection](#6-tips-for-best-detection)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. How Gesture Detection Works

The system uses Google MediaPipe to detect 21 landmark points on your hand in real time through the laptop webcam. Each point represents a key location on your hand such as fingertips, knuckles, wrist, and palm center.

The finger counting algorithm works by comparing the Y-coordinate of each fingertip landmark against the Y-coordinate of the corresponding knuckle landmark. If the fingertip is higher in the camera frame than the knuckle, that finger is counted as extended. The total number of extended fingers determines which gesture command is sent to the ESP32. The thumb is detected differently by comparing its X-coordinate position instead of Y-coordinate since the thumb moves sideways rather than upward.

---

## 2. Complete Gesture Reference

### Gesture 0 — Fist (All LEDs OFF)

How to do it: Close all fingers tightly into a fist with no fingers extended.

What happens: Both the Red LED and Green LED turn completely off.

Works when: This gesture works at all times, whether the system is locked or unlocked.

---

### Gesture 1 — One Finger (Red LED ON)

How to do it: Extend only your index finger and keep all other fingers folded down.

What happens: The Red LED representing the Living Room turns on at the brightness level of the current time mode.

Works when: This gesture only works when the system is in the unlocked state.

---

### Gesture 2 — Peace Sign (LOCK System)

How to do it: Extend your index finger and middle finger together in a V shape while keeping the other fingers folded.

What happens: The system enters the locked state. The current LED state is frozen and no further gesture commands are accepted until the system is unlocked.

Works when: This gesture works at all times including when already locked.

On screen: The status bar turns red and displays LOCKED.

---

### Gesture 3 — Three Fingers (Green LED ON)

How to do it: Extend your index finger, middle finger, and ring finger together while keeping the thumb and pinky folded.

What happens: The Green LED representing the Bedroom turns on at the brightness level of the current time mode.

Works when: This gesture only works when the system is in the unlocked state.

---

### Gesture 5 — Open Palm (UNLOCK System)

How to do it: Open all five fingers fully and spread them out clearly toward the camera.

What happens: The system exits the locked state, all LEDs are reset to off, and normal gesture control resumes immediately.

Works when: This gesture works at all times and is the only way to exit the locked state.

On screen: The status bar turns green and displays UNLOCKED.

---

## 3. Brightness Modes

The same gesture produces different brightness levels depending on the time of day. This is the Context-Aware Brightness feature of the project.

### Automatic Time-Based Modes

Morning mode runs from 6 AM to 12 PM and sets LED brightness to 100 percent with a PWM value of 255. This provides full brightness needed for activities and alertness during morning hours.

Afternoon mode runs from 12 PM to 6 PM and sets LED brightness to 78 percent with a PWM value of 200. Brightness is slightly reduced since ambient daylight provides natural supplementation.

Evening mode runs from 6 PM to 10 PM and sets LED brightness to 50 percent with a PWM value of 128. Half brightness is used for comfortable ambient lighting during relaxation hours.

Night mode runs from 10 PM to 6 AM and sets LED brightness to 20 percent with a PWM value of 50. Minimal brightness is used to preserve melatonin levels and support healthy sleep.

### How to Demonstrate the Brightness Innovation

Press M on the keyboard to activate Morning mode. Show one finger toward the camera and observe the Red LED at full brightness. Then press E to switch to Evening mode and show the same one finger gesture. The Red LED will visibly dim to half brightness. Finally press N for Night mode and show the same gesture again. The LED becomes very dim. This demonstrates that the same gesture, with the same device, produces three completely different brightness levels based on context.

---

## 4. Lock and Unlock System

The Gesture Lock System was designed to solve the accidental triggering problem. When users move their hands near the camera during normal activities, unintended gestures can accidentally change the LED state. The lock system prevents this completely.

When the system is in the unlocked state, all gestures work normally and control the LEDs. When the user shows a peace sign with two fingers, the system immediately enters the locked state. In the locked state, every subsequent gesture including fist, one finger, and three fingers is completely ignored. The LED state that was active at the moment of locking is frozen and maintained. The only gesture that has any effect while locked is the open palm with five fingers, which unlocks the system and resets all LEDs to off.

### How to Demonstrate the Lock Innovation

First turn on the Red LED using one finger gesture. Then show the peace sign to lock the system and observe the screen turning red with the LOCKED status. Wave your hand wildly in front of the camera and observe that the LED does not change at all. Ask another person to wave their hand near the camera and again observe no change. Finally show the open palm gesture to unlock the system and observe the screen turning green with the UNLOCKED status. Normal gesture control resumes immediately.

---

## 5. Keyboard Controls

The following keyboard keys can be pressed while the webcam window is open to manually override the automatic time-based brightness mode.

Press M to activate Morning mode at 100 percent brightness.

Press A to activate Afternoon mode at 78 percent brightness.

Press E to activate Evening mode at 50 percent brightness.

Press N to activate Night mode at 20 percent brightness.

Press X to return to automatic time-based mode where the system selects the brightness based on the current system clock.

Press Q to quit the program and close the webcam window.

---

## 6. Tips for Best Detection

Make sure the room has good lighting. The camera needs to clearly see your hand, so avoid sitting with a bright window behind you as this creates a silhouette effect that reduces detection accuracy.

Hold your hand at a distance of about 30 to 50 centimeters from the webcam. Too close causes the hand to go out of frame and too far reduces landmark accuracy.

Make each gesture clearly and hold it steady for at least half a second. The system has a 0.5 second debounce timer to prevent accidental repeated commands, so a quick flash of fingers may not register.

Keep your hand in the center of the camera frame where the detection model performs best. The green skeleton overlay on screen confirms when your hand is being tracked successfully.

For the peace sign gesture used for locking, make sure the V shape of your two fingers is clearly visible and spread apart so the system does not confuse it with a one-finger gesture.

For the open palm gesture used for unlocking, spread all five fingers as wide as possible so all five fingertips are clearly above their corresponding knuckles in the camera view.

---

## 7. Troubleshooting

If no hand skeleton appears on screen, check that the webcam is working and that lighting in the room is sufficient. Try moving closer to the camera or turning on a light.

If gestures are detected incorrectly, try slowing down your hand movements and holding each gesture more steadily. Make sure your hand is fully visible without any fingers going out of frame.

If the LED does not respond to gestures, check that the system status bar shows UNLOCKED in green. If it shows LOCKED in red, show an open palm to unlock first.

If the program shows ESP32 not found when starting, make sure the USB cable is plugged in, the Arduino Serial Monitor is completely closed, and the correct COM port is detected.

If mediapipe shows an attribute error, run the command pip install mediapipe==0.10.13 in the terminal to install the correct compatible version.

---

*AI-Powered Gesture Controlled Smart Home System — VIT Bhopal University — ECE Project 2025-2026*
