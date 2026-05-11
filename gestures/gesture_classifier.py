import math
import time

class GestureClassifier:

    def __init__(self):
        self.pinch_frames = 0
        self.drag_active = False
        self.drag_start_frames = 5
        self.click_max_frames = 4
        self.last_click_time = 0
        self.last_click_was_recent = False
        self.double_click_window = 0.35
        self.last_scroll_time = 0
        self.scroll_delay = 0.08
        self.last_volume_time = 0
        self.volume_delay = 0.4

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def classify(self, fingers, lm):
        if not lm or not fingers:
            self.pinch_frames = 0
            self.drag_active = False
            return None

        thumb  = lm[4]
        index  = lm[8]
        middle = lm[12]
        palm   = lm[9]

        hand_size = self.distance(palm, index)
        pinch_distance = self.distance(thumb, index)
        pinch_threshold = hand_size * 0.28
        is_pinch = pinch_distance < pinch_threshold and fingers[1] == 1

        # PINCH → click / drag
        if is_pinch:
            self.pinch_frames += 1
            if self.pinch_frames >= self.drag_start_frames:
                self.drag_active = True
                return "DRAG"
            return None

        if self.pinch_frames > 0:
            if self.pinch_frames <= self.click_max_frames:
                current_time = time.time()
                self.pinch_frames = 0
                self.drag_active = False
                if self.last_click_was_recent and (current_time - self.last_click_time) < self.double_click_window:
                    self.last_click_was_recent = False
                    return "DOUBLE_CLICK"
                self.last_click_time = current_time
                self.last_click_was_recent = True
                return "CLICK"
            self.pinch_frames = 0
            self.drag_active = False

        # 2 fingers → SCROLL
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            now = time.time()
            if now - self.last_scroll_time > self.scroll_delay:
                self.last_scroll_time = now
                return "SCROLL_UP" if index[1] < palm[1] - hand_size * 0.1 else "SCROLL_DOWN"
            return None

        # 3 fingers → VOLUME UP
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            now = time.time()
            if now - self.last_volume_time > self.volume_delay:
                self.last_volume_time = now
                return "VOLUME_UP"
            return None

        # 4 fingers → VOLUME DOWN
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            now = time.time()
            if now - self.last_volume_time > self.volume_delay:
                self.last_volume_time = now
                return "VOLUME_DOWN"
            return None

        # Pinky only → SCREENSHOT
        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            return "SCREENSHOT"

        # Shaka 🤙 → SWITCH WINDOW
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            return "SWITCH_WINDOW"

        # Thumb + middle pinch → RIGHT CLICK
        if self.distance(thumb, middle) < hand_size * 0.25 and fingers[2] == 1:
            return "RIGHT_CLICK"

        # Index only → MOVE
        if fingers[1] == 1 and fingers[2] == 0:
            return "MOVE"

        return None