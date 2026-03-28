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
            return "NO HAND DETECTED"

        wrist = lm[0]
        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        palm = lm[9]

        hand_size = self.distance(wrist, palm)

        if fingers[0] == 1 and sum(fingers) == 1:
            if thumb[1] < wrist[1] - 10:
                return "THUMBS UP"
            elif thumb[1] > wrist[1] + 10:
                return "THUMBS DOWN"

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
            move = self.distance(wrist, self.prev_pos)
            if move > hand_size * 0.2:
                self.prev_pos = wrist
                return "HAND IS MOVING"

        self.prev_pos = wrist

        return "HAND DETECTED"

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

        if self.stable_count >= 2:
            self.cooldown = 8   # blocks next few frames
            return raw

        return None