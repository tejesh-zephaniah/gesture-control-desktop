import math

class GestureClassifier:

    def __init__(self):
        self.prev_pos = None

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def classify(self, fingers, lm):
        if not lm:
            return "NO HAND DETECTED"

        wrist = lm[0]
        thumb_tip = lm[4]

        # 👍 / 👎 THUMB DETECTION
        if fingers[0] == 1 and sum(fingers) == 1:
            if thumb_tip[1] < wrist[1]:
                return "THUMBS UP"
            else:
                return "THUMBS DOWN"

        # ✋ HAND MOVING
        if self.prev_pos:
            move = self.distance(wrist, self.prev_pos)
            if move > 20:
                self.prev_pos = wrist
                return "HAND IS MOVING"

        self.prev_pos = wrist

        # ✋ HAND ACTIVE
        if fingers and sum(fingers) == 5:
            return "HAND ACTIVE"

        # 🤏 CLICK (thumb + index)
        if self.distance(lm[4], lm[8]) < 40:
            return "CLICK"

        # 🤏 RIGHT CLICK (thumb + middle)
        if self.distance(lm[4], lm[12]) < 40:
            return "RIGHT CLICK"

        return "HAND DETECTED"