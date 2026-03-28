class GestureClassifier:

    def __init__(self):
        pass

    def classify(self, fingers, lm):
        if fingers is None:
            return "NO HAND"

        if fingers[0] == 1 and sum(fingers) == 1:
            return "THUMBS_UP"

        if fingers[1] == 1 and sum(fingers) == 1:
            return "MOVE"

        if fingers[1] == 1 and fingers[2] == 1:
            return "CLICK"

        if fingers[0] == 1 and fingers[1] == 1:
            return "RIGHT_CLICK"

        if sum(fingers) == 5:
            return "PALM"

        return "UNKNOWN"