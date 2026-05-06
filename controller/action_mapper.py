from controller.input_controller import InputController

class ActionMapper:

    def __init__(self):
        self.controller = InputController()
        self.freeze = False

    def execute(self, gesture, landmarks, frame_shape):
        if not landmarks:
            return

        x, y = landmarks[8]
        h, w, _ = frame_shape

        if gesture == "MOVE":
            self.freeze = False
            self.controller.move_cursor(x, y, w, h)

        elif gesture == "CLICK":
            self.freeze = True
            self.controller.left_click()

        elif gesture == "RIGHT CLICK":
            self.freeze = True
            self.controller.right_click()