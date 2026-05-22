import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import time
from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
from vision.landmark_processor import LandmarkProcessor
from controller.action_mapper import ActionMapper
from gestures.gesture_classifier import GestureClassifier

camera = CameraManager()
vision = HandDetector()
processor = LandmarkProcessor()
mapper = ActionMapper()
classifier = GestureClassifier()

last_x, last_y = None, None
current_gesture = None
gesture_display_time = 0
fps_time = time.time()
fps = 0
frame_count = 0

GESTURE_COLORS = {
    "MOVE":          (0, 255, 100),
    "CLICK":         (0, 200, 255),
    "DOUBLE_CLICK":  (0, 100, 255),
    "RIGHT_CLICK":   (0, 50, 200),
    "DRAG":          (255, 165, 0),
    "SCROLL_UP":     (100, 255, 50),
    "SCROLL_DOWN":   (50, 200, 50),
    "VOLUME_UP":     (255, 255, 0),
    "VOLUME_DOWN":   (200, 200, 0),
    "THUMBS_UP":     (0, 255, 0),
    "THUMBS_DOWN":   (0, 0, 255),
    "PEACE_SIGN":    (255, 0, 255),
    "SHUTDOWN":      (0, 0, 100),
}

while True:
    ret, frame = camera.read_frame()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_count += 1
    if time.time() - fps_time >= 1.0:
        fps = frame_count
        frame_count = 0
        fps_time = time.time()

    results = vision.process(frame)
    landmarks = processor.extract_landmarks(results, frame.shape)

    if landmarks:
        last_x = (landmarks[0][0] + landmarks[9][0]) // 2
        last_y = (landmarks[0][1] + landmarks[9][1]) // 2

    fingers = processor.get_finger_states(landmarks)
    
    # Extract all hands for two-hand gesture detection
    all_hands_landmarks = []
    if results and results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            hand_lms = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks]
            all_hands_landmarks.append(hand_lms)
    
    gesture = classifier.classify(fingers, landmarks, all_hands_landmarks)

    if gesture:
        current_gesture = gesture
        gesture_display_time = time.time()

    mapper.execute(gesture, landmarks, frame.shape)
    vision.draw(frame, results)

    h, w, _ = frame.shape
    cv2.putText(frame, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)

    if current_gesture and (time.time() - gesture_display_time < 1.0):
        color = GESTURE_COLORS.get(current_gesture, (255, 255, 255))
        label = current_gesture.replace("_", " ")
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.1, 2)
        cv2.rectangle(frame, (10, h - 60), (20 + tw, h - 20), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, h - 60), (20 + tw, h - 20), color, 2)
        cv2.putText(frame, label, (15, h - 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 2)

    cheat = [
        "1 finger = MOVE",
        "Pinch = CLICK",
        "2 fingers = VOL UP",
        "3 fingers = VOL DOWN",
        "Thumbs up = MUTE",
        "Thumbs down = UNMUTE",
        "2-Hand Peace = SCREENSHOT",
        "2-Hand Twist = SHUTDOWN",
    ]
    for i, line in enumerate(cheat):
        cv2.putText(frame, line, (w - 230, 25 + i * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (150, 150, 150), 1)

    cv2.imshow("Gesture Control Desktop", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()