from controller.input_controller import InputController

class ActionMapper:

    def __init__(self):
        self.controller = InputController()
        self.dragging = False

    def execute(self, gesture, landmarks, frame_shape):
        if gesture is None:
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            return

        if not landmarks:
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            return

        x, y = landmarks[8]
        h, w, _ = frame_shape

        if gesture == "MOVE":
            self.controller.move_cursor(x, y, w, h)

        elif gesture == "DRAG":
            if not self.dragging:
                self.controller.mouse_down()
                self.dragging = True
            self.controller.move_cursor(x, y, w, h)

        elif gesture == "CLICK":
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            self.controller.left_click()

        elif gesture == "DOUBLE_CLICK":
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            self.controller.double_click()

        elif gesture == "RIGHT CLICK":
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            self.controller.right_click()