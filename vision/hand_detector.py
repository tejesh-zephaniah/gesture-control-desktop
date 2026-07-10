import cv2
import mediapipe as mp
import sys
from pathlib import Path

class HandDetector:
    def __init__(self):
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        self.BaseOptions = python.BaseOptions
        self.HandLandmarker = vision.HandLandmarker
        self.HandLandmarkerOptions = vision.HandLandmarkerOptions
        self.VisionRunningMode = vision.RunningMode

        self.latest_result = None

        def callback(result, output_image, timestamp_ms):
            self.latest_result = result

        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
        model_path = base_path / "hand_landmarker.task"

        if not model_path.exists():
            raise FileNotFoundError(f"hand_landmarker.task not found at {model_path}")

        self.options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(
                model_asset_path=str(model_path)
            ),
            num_hands=2,
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=callback
        )

        self.detector = self.HandLandmarker.create_from_options(self.options)
        self.timestamp = 0

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp += 1
        self.detector.detect_async(mp_image, self.timestamp)

        return self.latest_result

    def draw(self, frame, results):
        if results and results.hand_landmarks:
            h, w, _ = frame.shape

            for hand_landmarks in results.hand_landmarks:
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)