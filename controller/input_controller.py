import pyautogui
from utils.smoothing import Smoother

class InputController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.PAUSE = 0
        self.smoother = Smoother(alpha=0.2)

    def move_cursor(self, x, y, frame_width, frame_height):

        x, y = self.smoother.smooth(x, y)

        margin_x = 0.02 * frame_width
        margin_y = 0.02 * frame_height

        usable_w = frame_width - 2 * margin_x
        usable_h = frame_height - 2 * margin_y

        x = max(margin_x, min(frame_width - margin_x, x))
        y = max(margin_y, min(frame_height - margin_y, y))

        norm_x = (x - margin_x) / usable_w
        norm_y = (y - margin_y) / usable_h

        gain = 1.8
        norm_x = 0.5 + (norm_x - 0.5) * gain
        norm_y = 0.5 + (norm_y - 0.5) * gain

        norm_x = max(0.001, min(0.999, norm_x))
        norm_y = max(0.001, min(0.999, norm_y))

        screen_x = int(norm_x * self.screen_width)
        screen_y = int(norm_y * self.screen_height)

        screen_x = max(1, min(self.screen_width - 1, screen_x))
        screen_y = max(1, min(self.screen_height - 1, screen_y))

        pyautogui.moveTo(screen_x, screen_y, duration=0)

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.rightClick()