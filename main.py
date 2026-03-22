#Setup template
import cv2
from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
from vision.landmark_processor import LandmarkProcessor
import mediapipe as mp

camera= CameraManager()
vision= HandDetector()
processor = LandmarkProcessor()

while True:
    ret, frame = camera.read_frame()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    results = vision.process(frame)
    landmarks = processor.extract_landmarks(results, frame.shape)
    fingers = processor.get_finger_states(landmarks)
    
    if landmarks:
        print(fingers)
        
    vision.draw(frame,results)
            
    cv2.imshow("Gesture-Control-Desktop", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()