import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
from vision.landmark_processor import LandmarkProcessor
from controller.action_mapper import ActionMapper

camera = CameraManager()
vision = HandDetector()
processor = LandmarkProcessor()
mapper = ActionMapper()

last_x, last_y = None, None

while True:
    ret, frame = camera.read_frame()

    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)

    results = vision.process(frame)
    landmarks = processor.extract_landmarks(results, frame.shape)

    if landmarks:
        x = (landmarks[0][0] + landmarks[9][0]) // 2
        y = (landmarks[0][1] + landmarks[9][1]) // 2
        last_x, last_y = x, y
    else:
        if last_x is None:
            continue
        x, y = last_x, last_y

    mapper.controller.move_cursor(x, y, frame.shape[1], frame.shape[0])

    vision.draw(frame, results)
    cv2.imshow("Gesture-Control-Desktop", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()