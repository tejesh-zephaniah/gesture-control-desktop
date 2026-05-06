import cv2

class CameraManager:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        # 🔥 reduce lag
        self.cap.set(3, 640)
        self.cap.set(4, 480)

    def read_frame(self):
        return self.cap.read()

    def release(self):
        self.cap.release()