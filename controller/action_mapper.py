from controller.input_controller import InputController

class ActionMapper:

    def __init__(self):
        self.controller = InputController()

    def execute(self, gesture, landmarks, frame_shape):
        if gesture == "MOVE" and landmarks:
            x, y = landmarks[8]
            h, w, _ = frame_shape
            self.controller.move_cursor(x, y, w, h)