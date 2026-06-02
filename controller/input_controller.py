import pyautogui
import time
import math
from datetime import datetime
import os
from pathlib import Path

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
        self.muted = False

    def move_cursor(self, x, y, frame_width, frame_height):
        nx = x / frame_width
        ny = y / frame_height

        # map directly to full camera frame (no margin) and clamp to [0,1]
        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))

        screen_x = int(nx * self.screen_width)
        screen_y = int(ny * self.screen_height)

        if self.prev_x is None or self.prev_y is None:
            self.prev_x, self.prev_y = screen_x, screen_y
            pyautogui.moveTo(screen_x, screen_y)
            return

        dx = screen_x - self.prev_x
        dy = screen_y - self.prev_y
        dist = math.hypot(dx, dy)

        if dist < 3:
            smooth = 1.0
        elif dist < 10:
            smooth = 0.8
        elif dist < 30:
            smooth = 0.6
        else:
            smooth = 0.45

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
        """Take a fullscreen screenshot and save to Pictures folder."""
        try:
            # Get Pictures folder path
            pictures_dir = Path.home() / "Pictures"
            pictures_dir.mkdir(exist_ok=True)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = pictures_dir / f"Screenshot_{timestamp}.png"
            
            # Take fullscreen screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(str(screenshot_path))
            
            print(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")

    def switch_window(self):
        pyautogui.hotkey('alt', 'tab')

    def mouse_down(self):
        if not self.dragging:
            self.dragging = True
            pyautogui.mouseDown(button='left')

    def mouse_up(self):
        if self.dragging:
            self.dragging = False
            pyautogui.mouseUp(button='left')

    def left_click(self):
        now = time.time()
        if now - self.last_click_time > self.click_delay:
            pyautogui.click(button='left')
            self.last_click_time = now

    def double_click(self):
        pyautogui.doubleClick()

    def right_click(self):
        pyautogui.click(button='right')

    def mute(self):
        pyautogui.press('volumemute')
        self.muted = True

    def unmute(self):
        pyautogui.press('volumemute')
        self.muted = False

