# ============================================================
# AI-Powered Gesture Controlled Smart Home System
# Main Python Script
#
# Authors: Manas Krishna Neigapula (24BEC10104)
#          Priyam Prakash (24BEC10139)
# Guide:   Prof. S.P. Manikandan
# Institution: VIT Bhopal University
#
# Description:
# Captures webcam frames, detects hand gestures using MediaPipe,
# applies context-aware brightness logic, and sends commands
# to ESP32 via serial communication.
#
# Gestures:
#   0 fingers (Fist)    → All LEDs OFF
#   1 finger            → Red LED ON
#   2 fingers (Peace)   → LOCK system
#   3 fingers           → Green LED ON
#   5 fingers (Palm)    → UNLOCK system
#
# Keyboard Controls:
#   M = Morning mode (100%)
#   A = Afternoon mode (78%)
#   E = Evening mode (50%)
#   N = Night mode (20%)
#   X = Auto time-based mode
#   Q = Quit
# ============================================================

import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
import time
from datetime import datetime

# ── Auto-detect ESP32 Port ────────────────────────────────────────────────────
def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Found port: {port.device} - {port.description}")
        if any(x in port.description for x in ['CH340', 'CP210', 'USB', 'UART', 'Silicon']):
            return port.device
    return 'COM3'  # Default fallback

# ── Initialize ESP32 Connection ───────────────────────────────────────────────
print("=" * 50)
print("  AI Gesture Smart Home System")
print("  VIT Bhopal University - ECE Project")
print("=" * 50)
print("\nStarting system...")
print("Connecting to ESP32...")

port = find_esp32_port()
print(f"Using port: {port}")

try:
    esp32 = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)
    print("ESP32 Connected Successfully!")
except Exception as e:
    print(f"\nERROR connecting to ESP32: {e}")
    print("SOLUTION: Make sure Arduino Serial Monitor is CLOSED")
    exit()

# ── MediaPipe Setup ───────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    static_image_mode        = False,
    max_num_hands            = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence  = 0.7
)

# ── Webcam Setup ──────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Camera 0 not found. Trying camera 1...")
    cap = cv2.VideoCapture(1)

print("Webcam opened!")

# ── Context: Time-Based Brightness ───────────────────────────────────────────
def get_time_mode():
    """Returns mode name and PWM brightness based on current time."""
    hour = datetime.now().hour
    if   6  <= hour < 12: return "MORNING",   255   # 100%
    elif 12 <= hour < 18: return "AFTERNOON", 200   # 78%
    elif 18 <= hour < 22: return "EVENING",   128   # 50%
    else:                 return "NIGHT",      50   # 20%

# ── Finger Counting Algorithm ─────────────────────────────────────────────────
def count_fingers(hand_landmarks):
    """
    Counts extended fingers by comparing fingertip Y-coordinate
    against the corresponding knuckle Y-coordinate.
    Returns integer 0-5.
    """
    fingertip_ids = [8, 12, 16, 20]   # Index, Middle, Ring, Pinky
    count = 0

    # Thumb: compare X-coordinates (horizontal extension)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1

    # Other four fingers: compare Y-coordinates (vertical extension)
    for tip_id in fingertip_ids:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            count += 1

    return count

# ── Send Command to ESP32 ─────────────────────────────────────────────────────
def send_command(led, brightness):
    """Sends LED:BRIGHTNESS command to ESP32 over serial."""
    try:
        command = f"{led}:{brightness}\n"
        esp32.write(command.encode())
        print(f"  → Sent: {command.strip()}")
    except Exception as e:
        print(f"  ✗ Serial error: {e}")

# ── State Variables ───────────────────────────────────────────────────────────
locked           = False
last_gesture     = -1
last_send_time   = 0
manual_mode      = None
manual_brightness = None

print("\n" + "=" * 50)
print("SYSTEM READY — Show hand gestures to webcam!")
print("=" * 50)
print("  Fist      → All OFF")
print("  1 Finger  → Red LED ON")
print("  2 Fingers → LOCK")
print("  3 Fingers → Green LED ON")
print("  5 Fingers → UNLOCK")
print("\nKeys: M A E N = modes | X = auto | Q = quit")
print("=" * 50 + "\n")

# ── Main Loop ─────────────────────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera read error!")
        break

    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    result = hands.process(rgb_frame)

    # Determine current brightness mode
    if manual_mode:
        mode_name  = manual_mode
        brightness = manual_brightness
    else:
        mode_name, brightness = get_time_mode()

    finger_count  = -1
    gesture_text  = "No Hand Detected"

    # ── Gesture Detection ─────────────────────────────────────────────────────
    if result.multi_hand_landmarks:
        for hand_lm in result.multi_hand_landmarks:

            # Draw hand skeleton on frame
            mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

            # Count extended fingers
            finger_count = count_fingers(hand_lm)

            # Map finger count to gesture label
            gesture_map = {
                0: "FIST - All OFF",
                1: "1 Finger - Red LED ON",
                2: "Peace Sign - LOCK",
                3: "3 Fingers - Green LED ON",
                5: "Open Palm - UNLOCK"
            }
            gesture_text = gesture_map.get(finger_count, f"{finger_count} Fingers")

            # ── Debounce + Send Command ───────────────────────────────────────
            current_time = time.time()
            gesture_changed = finger_count != last_gesture
            debounce_passed = (current_time - last_send_time) > 0.5

            if gesture_changed and debounce_passed:
                last_gesture   = finger_count
                last_send_time = current_time

                if finger_count == 2:
                    # LOCK
                    locked = True
                    print("🔒 SYSTEM LOCKED")

                elif finger_count == 5:
                    # UNLOCK
                    locked = False
                    send_command(0, 0)
                    print("🔓 SYSTEM UNLOCKED")

                elif not locked:
                    if   finger_count == 0: send_command(0, 0)
                    elif finger_count == 1: send_command(1, brightness)
                    elif finger_count == 3: send_command(3, brightness)

    # ── Keyboard Controls ─────────────────────────────────────────────────────
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Quitting...")
        break
    elif key == ord('m'):
        manual_mode, manual_brightness = "MORNING", 255
        print("Mode: MORNING (100%)")
    elif key == ord('a'):
        manual_mode, manual_brightness = "AFTERNOON", 200
        print("Mode: AFTERNOON (78%)")
    elif key == ord('e'):
        manual_mode, manual_brightness = "EVENING", 128
        print("Mode: EVENING (50%)")
    elif key == ord('n'):
        manual_mode, manual_brightness = "NIGHT", 50
        print("Mode: NIGHT (20%)")
    elif key == ord('x'):
        manual_mode = None
        print("Mode: AUTO (time-based)")

    # ── On-Screen Display ─────────────────────────────────────────────────────
    lock_color = (0, 0, 255) if locked else (0, 255, 0)
    lock_text  = "LOCKED"   if locked else "UNLOCKED"

    # Black info bar at top
    cv2.rectangle(frame, (0, 0), (640, 130), (0, 0, 0), -1)

    cv2.putText(frame, f"Gesture: {gesture_text}",
                (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.putText(frame, f"Mode: {mode_name}  |  Brightness: {brightness}",
                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

    cv2.putText(frame, f"Status: {lock_text}",
                (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.75, lock_color, 2)

    cv2.imshow("AI Gesture Smart Home — VIT Bhopal", frame)

# ── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
esp32.close()
cv2.destroyAllWindows()
print("\nSystem stopped. Goodbye!")
