import pyautogui
import time
import math

class InputController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

        self.prev_x = None
        self.prev_y = None

        self.last_click_time = 0
        self.click_delay = 0.25
        self.dragging = False

    def move_cursor(self, x, y, frame_width, frame_height):

        nx = x / frame_width
        ny = y / frame_height

        # FIX: 0.05 instead of 0.15 → cursor can now reach top of screen
        margin = 0.05

        nx = (nx - margin) / (1 - 2 * margin)
        ny = (ny - margin) / (1 - 2 * margin)

        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))

        screen_x = int(nx * self.screen_width)
        screen_y = int(ny * self.screen_height)

        if self.prev_x is None:
            self.prev_x, self.prev_y = screen_x, screen_y

        dx = screen_x - self.prev_x
        dy = screen_y - self.prev_y
        dist = math.hypot(dx, dy)

        # FIX: snap factor 0.8 for big jumps → no more lag
        if dist < 3:
            smooth = 0.1
        elif dist < 10:
            smooth = 0.3
        elif dist < 30:
            smooth = 0.5
        else:
            smooth = 0.8

        smooth_x = int(self.prev_x + dx * smooth)
        smooth_y = int(self.prev_y + dy * smooth)

        self.prev_x, self.prev_y = smooth_x, smooth_y
        pyautogui.moveTo(smooth_x, smooth_y)

    def scroll(self, direction, amount=3):
        pyautogui.scroll(amount if direction == 'up' else -amount)

    def volume_up(self):
        pyautogui.press('volumeup')

    def volume_down(self):
        pyautogui.press('volumedown')

    def screenshot(self):
        pyautogui.hotkey('win', 'shift', 's')

    def switch_window(self):
        pyautogui.hotkey('alt', 'tab')

    def mouse_down(self):
        if not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True

    def mouse_up(self):
        if self.dragging:
            pyautogui.mouseUp()
            self.dragging = False

    def left_click(self):
        now = time.time()
        if now - self.last_click_time > self.click_delay:
            pyautogui.click()
            self.last_click_time = now

    def double_click(self):
        pyautogui.click(clicks=2, interval=0.1)

    def right_click(self):
        pyautogui.rightClick()