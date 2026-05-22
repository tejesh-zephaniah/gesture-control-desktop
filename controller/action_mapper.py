from controller.input_controller import InputController
import time

class ActionMapper:

    def __init__(self):
        self.controller = InputController()
        self.dragging = False

        self.cursor_smoothness = 0.55
        self.dead_zone = 4
        self.last_move_point = None

    def _smooth_point(self, x, y):
        if self.last_move_point is None:
            self.last_move_point = (x, y)
            return x, y

        lx, ly = self.last_move_point
        dx = x - lx
        dy = y - ly

        if abs(dx) < self.dead_zone and abs(dy) < self.dead_zone:
            return lx, ly

        nx = int(lx + dx * self.cursor_smoothness)
        ny = int(ly + dy * self.cursor_smoothness)
        self.last_move_point = (nx, ny)
        return nx, ny

    def execute(self, gesture, landmarks, frame_shape):
        if gesture is None or not landmarks:
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            return

        x, y = landmarks[8]
        h, w, _ = frame_shape

        if gesture == "MOVE":
            x, y = self._smooth_point(x, y)
            self.controller.move_cursor(x, y, w, h)

        elif gesture == "DRAG":
            if not self.dragging:
                self.controller.mouse_down()
                self.dragging = True
            x, y = self._smooth_point(x, y)
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

        elif gesture == "RIGHT_CLICK":
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            self.controller.right_click()

        elif gesture == "VOLUME_UP":
            self.controller.volume_up()

        elif gesture == "VOLUME_DOWN":
            self.controller.volume_down()

        elif gesture == "THUMBS_UP":
            self.controller.mute()

        elif gesture == "THUMBS_DOWN":
            self.controller.unmute()

        elif gesture == "PEACE_SIGN":
            self.controller.screenshot()

        elif gesture == "SHUTDOWN":
            self.controller.shutdown()