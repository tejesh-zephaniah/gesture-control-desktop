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

    def move_cursor(self, x, y, frame_width, frame_height):

        # --- 1. normalize ---
        nx = x / frame_width
        ny = y / frame_height

        # --- 2. bigger margin = LOWER sensitivity ---
        margin = 0.2   # 🔥 increased (was 0.1)

        nx = (nx - margin) / (1 - 2 * margin)
        ny = (ny - margin) / (1 - 2 * margin)

        nx = max(0, min(1, nx))
        ny = max(0, min(1, ny))

        # --- 3. aspect ratio fix ---
        cam_ratio = frame_width / frame_height
        screen_ratio = self.screen_width / self.screen_height

        if cam_ratio > screen_ratio:
            scale = screen_ratio / cam_ratio
            nx = 0.5 + (nx - 0.5) * scale
        else:
            scale = cam_ratio / screen_ratio
            ny = 0.5 + (ny - 0.5) * scale

        # --- 4. map ---
        screen_x = int(nx * self.screen_width)
        screen_y = int(ny * self.screen_height)

        if self.prev_x is None:
            self.prev_x, self.prev_y = screen_x, screen_y

        dx = screen_x - self.prev_x
        dy = screen_y - self.prev_y

        dist = math.hypot(dx, dy)

        # --- 5. MORE smoothing (reduces sensitivity) ---
        if dist < 10:
            smooth = 0.08   # 🔥 very slow, high precision
        elif dist < 40:
            smooth = 0.15
        else:
            smooth = 0.25

        smooth_x = int(self.prev_x + dx * smooth)
        smooth_y = int(self.prev_y + dy * smooth)

        self.prev_x, self.prev_y = smooth_x, smooth_y

        pyautogui.moveTo(smooth_x, smooth_y)

    def left_click(self):
        now = time.time()
        if now - self.last_click_time > self.click_delay:
            pyautogui.click()
            self.last_click_time = now

    def right_click(self):
        pyautogui.rightClick()