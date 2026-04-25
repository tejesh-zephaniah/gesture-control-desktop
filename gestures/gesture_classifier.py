import math

class GestureClassifier:

    def __init__(self):
        self.prev_pos = None
        self.last_gesture = None
        self.stable_count = 0
        self.cooldown = 0

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def classify_raw(self, fingers, lm):
        if not lm:
            return None

        pos = lm[8]  # index finger tip
        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        palm = lm[9]

        hand_size = self.distance(palm, index)

        if fingers and sum(fingers) == 5:
            return "HAND ACTIVE"

        if (
            self.distance(thumb, index) < hand_size * 0.3 and
            fingers[0] == 1 and fingers[1] == 1
        ):
            return "CLICK"

        if (
            self.distance(thumb, middle) < hand_size * 0.3 and
            fingers[0] == 1 and fingers[2] == 1
        ):
            return "RIGHT CLICK"

        if self.prev_pos:
            move = self.distance(pos, self.prev_pos)
            if move > hand_size * 0.08:
                self.prev_pos = pos
                return "MOVE"

        self.prev_pos = pos

        return None

    def classify(self, fingers, lm):
        raw = self.classify_raw(fingers, lm)

        if raw == self.last_gesture:
            self.stable_count += 1
        else:
            self.stable_count = 0

        self.last_gesture = raw

        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        if self.stable_count >= 1:
            self.cooldown = 2
            return raw

        return None