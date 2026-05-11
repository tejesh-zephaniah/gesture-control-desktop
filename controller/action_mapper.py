from controller.input_controller import InputController
import time

class ActionMapper:

    def __init__(self):
        self.controller = InputController()
        self.dragging = False
        self.last_screenshot_time = 0
        self.screenshot_delay = 1.5
        self.last_switch_time = 0
        self.switch_delay = 0.8

    def execute(self, gesture, landmarks, frame_shape):
        if gesture is None or not landmarks:
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

        elif gesture == "RIGHT_CLICK":
            if self.dragging:
                self.controller.mouse_up()
                self.dragging = False
            self.controller.right_click()

        elif gesture == "SCROLL_UP":
            self.controller.scroll('up', amount=4)

        elif gesture == "SCROLL_DOWN":
            self.controller.scroll('down', amount=4)

        elif gesture == "VOLUME_UP":
            self.controller.volume_up()

        elif gesture == "VOLUME_DOWN":
            self.controller.volume_down()

        elif gesture == "SCREENSHOT":
            now = time.time()
            if now - self.last_screenshot_time > self.screenshot_delay:
                self.last_screenshot_time = now
                self.controller.screenshot()

        elif gesture == "SWITCH_WINDOW":
            now = time.time()
            if now - self.last_switch_time > self.switch_delay:
                self.last_switch_time = now
                self.controller.switch_window()