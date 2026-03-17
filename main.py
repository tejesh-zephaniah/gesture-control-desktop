#Setup template
import cv2
from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
import mediapipe as mp

camera= CameraManager()
vision= HandDetector()

while True:
    ret, frame = camera.read_frame()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    results = vision.process(frame)
    vision.draw(frame,results)
            
    cv2.imshow("Gesture-Control-Desktop", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()