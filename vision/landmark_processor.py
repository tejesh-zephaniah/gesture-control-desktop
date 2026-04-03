import math
from collections import deque

class LandmarkProcessor:

    def __init__(self):
        self.history = deque(maxlen=7)  # more frames = more stability


    def extract_landmarks(self, results, frame_shape):
        landmark_list = []

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                for lm in hand_landmarks:
                    h, w, _ = frame_shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append((cx, cy))

        return landmark_list


    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


    def angle(self, a, b, c):
        ab = (a[0] - b[0], a[1] - b[1])
        cb = (c[0] - b[0], c[1] - b[1])

        dot = ab[0]*cb[0] + ab[1]*cb[1]
        mag_ab = math.hypot(*ab)
        mag_cb = math.hypot(*cb)

        if mag_ab * mag_cb == 0:
            return 0

        cos_angle = dot / (mag_ab * mag_cb)
        cos_angle = max(-1, min(1, cos_angle))
        return math.degrees(math.acos(cos_angle))


    def is_finger_up(self, lm, tip, pip, mcp):
        wrist = lm[0]

        tip_pt = lm[tip]
        pip_pt = lm[pip]
        mcp_pt = lm[mcp]

        # distance ratio
        tip_dist = self.distance(wrist, tip_pt)
        pip_dist = self.distance(wrist, pip_pt)

        ratio = tip_dist / (pip_dist + 1e-6)

        # angle
        ang = self.angle(mcp_pt, pip_pt, tip_pt)

        # DEAD ZONE (prevents flicker)
        if 1.02 < ratio < 1.08:
            return None  # uncertain

        # final decision
        if ratio > 1.08 and ang > 150:
            return 1
        else:
            return 0


    def get_finger_states(self, lm):
        if not lm:
            return None

        fingers = [0, 0, 0, 0, 0]

        # THUMB (distance + angle combo)
        thumb_ratio = self.distance(lm[4], lm[0]) / (self.distance(lm[3], lm[0]) + 1e-6)
        thumb_angle = self.angle(lm[2], lm[3], lm[4])

        if thumb_ratio > 1.05 and thumb_angle > 140:
            fingers[0] = 1
        else:
            fingers[0] = 0

        finger_ids = [
            (8, 6, 5),
            (12, 10, 9),
            (16, 14, 13),
            (20, 18, 17)
        ]

        for i, (tip, pip, mcp) in enumerate(finger_ids, start=1):
            val = self.is_finger_up(lm, tip, pip, mcp)
            fingers[i] = val if val is not None else fingers[i]

        # SMOOTHING (major fix)
        self.history.append(fingers)

        smoothed = []
        for i in range(5):
            vals = [frame[i] for frame in self.history if frame[i] is not None]
            if len(vals) == 0:
                smoothed.append(0)
            else:
                smoothed.append(1 if sum(vals) > len(vals)//2 else 0)

        return smoothed