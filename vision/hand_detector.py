import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        self.BaseOptions = python.BaseOptions
        self.HandLandmarker = vision.HandLandmarker
        self.HandLandmarkerOptions = vision.HandLandmarkerOptions

        self.options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(
                model_asset_path="hand_landmarker.task"
            ),
            num_hands=2
        )

        self.detector = self.HandLandmarker.create_from_options(self.options)

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        results = self.detector.detect(mp_image)
        return results

    def draw(self, frame, results):
        if results.hand_landmarks:
            h, w, _ = frame.shape

            for hand_landmarks in results.hand_landmarks:
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)