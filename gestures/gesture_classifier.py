import math

class GestureClassifier:

    def __init__(self):
        self.last_click_time = 0
        self.click_delay = 0.3

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def classify(self, fingers, lm):
        if not lm or not fingers:
            return None

        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        palm = lm[9]

        hand_size = self.distance(palm, index)

        # 👆 LEFT CLICK (pinch)
        if (
            self.distance(thumb, index) < hand_size * 0.25 and
            fingers[1] == 1
        ):
            return "CLICK"

        # 👉 RIGHT CLICK
        if (
            self.distance(thumb, middle) < hand_size * 0.25 and
            fingers[2] == 1
        ):
            return "RIGHT CLICK"

        # ✋ MOVE when index finger is up
        if fingers[1] == 1:
            return "MOVE"

        return None