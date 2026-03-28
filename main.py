#setup Template
import cv2
from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
from vision.landmark_processor import LandmarkProcessor
from gestures.gesture_classifier import GestureClassifier

camera = CameraManager()
vision = HandDetector()
processor = LandmarkProcessor()
classifier = GestureClassifier()

prev_gesture = None

while True:
    ret, frame = camera.read_frame()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    results = vision.process(frame)
    landmarks = processor.extract_landmarks(results, frame.shape)
    fingers = processor.get_finger_states(landmarks)

    # ✅ unified gesture handling
    if landmarks and fingers:
        gesture = classifier.classify(fingers, landmarks)
    else:
        gesture = "NO HAND DETECTED"

    # ✅ print only when changed (VERY IMPORTANT)
    if gesture and gesture != prev_gesture:
        print("👉", gesture)
        prev_gesture = gesture

    vision.draw(frame, results)
    cv2.imshow("Gesture-Control-Desktop", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()