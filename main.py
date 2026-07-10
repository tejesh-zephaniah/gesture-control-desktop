import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import ctypes
import platform
import cv2
import numpy as np
import time

try:
    import tkinter as tk
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

from camera.camera_manager import CameraManager
from vision.hand_detector import HandDetector
from vision.landmark_processor import LandmarkProcessor
from controller.action_mapper import ActionMapper
from gestures.gesture_classifier import GestureClassifier

camera = CameraManager()
vision = HandDetector()
processor = LandmarkProcessor()
mapper = ActionMapper()
classifier = GestureClassifier()

last_x, last_y = None, None
current_gesture = None
gesture_display_time = 0
fps_time = time.time()
fps = 0
frame_count = 0

GESTURE_COLORS = {
    "MOVE":          (0, 255, 100),
    "CLICK":         (0, 200, 255),
    "DOUBLE_CLICK":  (0, 100, 255),
    "RIGHT_CLICK":   (0, 50, 200),
    "DRAG":          (255, 165, 0),
    "SCROLL_UP":     (100, 255, 50),
    "SCROLL_DOWN":   (50, 200, 50),
    "VOLUME_UP":     (255, 255, 0),
    "VOLUME_DOWN":   (200, 200, 0),
    "THUMBS_UP":     (0, 255, 0),
    "THUMBS_DOWN":   (0, 0, 255),
    "PEACE_SIGN":    (255, 0, 255),
}

def _set_borderless_window(window_name, x=0, y=0, width=None, height=None):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    if width is not None and height is not None:
        cv2.resizeWindow(window_name, width, height)
    cv2.moveWindow(window_name, x, y)

    if platform.system() != "Windows":
        return

    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
    if not hwnd:
        return

    GWL_STYLE = -16
    WS_POPUP = 0x80000000
    WS_VISIBLE = 0x10000000
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_NOACTIVATE = 0x0010
    SWP_FRAMECHANGED = 0x0020
    HWND_TOP = 0

    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~(0x00C00000 | 0x00040000 | 0x00020000 | 0x00010000)
    style |= WS_POPUP | WS_VISIBLE
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

    flags = SWP_NOACTIVATE | SWP_FRAMECHANGED
    if width is None or height is None:
        flags |= SWP_NOSIZE
    if x is None or y is None:
        flags |= SWP_NOMOVE

    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOP, x, y,
                                      width or 0, height or 0, flags)


def _rounded_panel(frame, radius=20, panel_bg=(30, 30, 30)):
    h, w = frame.shape[:2]
    panel = np.full((h, w, 3), panel_bg, dtype=np.uint8)
    mask = np.zeros((h, w), dtype=np.uint8)

    cv2.rectangle(mask, (radius, 0), (w - radius, h), 255, -1)
    cv2.rectangle(mask, (0, radius), (w, h - radius), 255, -1)
    cv2.circle(mask, (radius, radius), radius, 255, -1)
    cv2.circle(mask, (w - radius, radius), radius, 255, -1)
    cv2.circle(mask, (radius, h - radius), radius, 255, -1)
    cv2.circle(mask, (w - radius, h - radius), radius, 255, -1)

    panel[mask == 255] = frame[mask == 255]
    return panel


WINDOW_NAME = "Gesture Control Desktop"

GESTURE_REFERENCE = [
    ("1 finger", "MOVE cursor"),
    ("Pinch", "LEFT CLICK"),
    ("Hold pinch and move", "DRAG"),
    ("2 fingers", "VOLUME UP"),
    ("3 fingers", "VOLUME DOWN"),
    ("Thumbs up", "MUTE"),
    ("Thumbs down", "UNMUTE"),
    ("Two-hand peace", "SCREENSHOT"),
]

sidebar_root = None
sidebar_width = 260
sidebar_padding = 12
sidebar_line_height = 28
sidebar_title_height = 40
sidebar_height = sidebar_title_height + len(GESTURE_REFERENCE) * sidebar_line_height + sidebar_padding * 2
camera_width = 360
camera_height = 270
camera_x_offset = 0
camera_y_offset = sidebar_height + 8
_set_borderless_window(WINDOW_NAME, camera_x_offset, camera_y_offset, camera_width, camera_height)


def _create_sidebar_window(width, height, x_offset, y_offset=0):
    if not TK_AVAILABLE:
        return None

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.96)
    root.configure(bg="#000001")
    if platform.system() == "Windows":
        root.wm_attributes("-transparentcolor", "#000001")
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
    root.lift()
    root.attributes("-disabled", False)
    root.update_idletasks()

    canvas = tk.Canvas(root, width=width, height=height, bg="#000001", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    radius = 18
    fill = "#232323"
    canvas.create_rectangle(radius, 0, width - radius, height, fill=fill, width=0)
    canvas.create_rectangle(0, radius, width, height - radius, fill=fill, width=0)
    canvas.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill=fill, outline=fill)
    canvas.create_arc(width - radius * 2, 0, width, radius * 2, start=0, extent=90, fill=fill, outline=fill)
    canvas.create_arc(0, height - radius * 2, radius * 2, height, start=180, extent=90, fill=fill, outline=fill)
    canvas.create_arc(width - radius * 2, height - radius * 2, width, height, start=270, extent=90, fill=fill, outline=fill)

    title = tk.Label(root, text="GESTURE REFERENCE", fg="#f2f2f2", bg=fill,
                     font=("Segoe UI", 10, "bold"))
    canvas.create_window(16, 18, anchor="nw", window=title)

    offset_y = 42
    for label, action in GESTURE_REFERENCE:
        left = tk.Label(root, text=label, fg="#ffffff", bg=fill, anchor="w",
                        width=16, font=("Segoe UI", 9))
        right = tk.Label(root, text=action, fg="#d4d4d4", bg=fill, anchor="w",
                         width=12, font=("Segoe UI", 9))
        canvas.create_window(16, offset_y, anchor="nw", window=left)
        canvas.create_window(150, offset_y, anchor="nw", window=right)
        offset_y += 26

    return root


while True:
    ret, frame = camera.read_frame()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_count += 1
    if time.time() - fps_time >= 1.0:
        fps = frame_count
        frame_count = 0
        fps_time = time.time()

    results = vision.process(frame)
    landmarks = processor.extract_landmarks(results, frame.shape)

    if landmarks:
        last_x = (landmarks[0][0] + landmarks[9][0]) // 2
        last_y = (landmarks[0][1] + landmarks[9][1]) // 2

    fingers = processor.get_finger_states(landmarks)
    
    # Extract all hands for two-hand gesture detection
    all_hands_landmarks = []
    if results and results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            hand_lms = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks]
            all_hands_landmarks.append(hand_lms)
    
    gesture = classifier.classify(fingers, landmarks, all_hands_landmarks)

    if gesture:
        current_gesture = gesture
        gesture_display_time = time.time()

    mapper.execute(gesture, landmarks, frame.shape)
    vision.draw(frame, results)

    h, w, _ = frame.shape
    if TK_AVAILABLE and sidebar_root is None:
        try:
            sidebar_root = _create_sidebar_window(sidebar_width, sidebar_height, 0, 0)
        except Exception:
            sidebar_root = None

    if TK_AVAILABLE and sidebar_root is not None:
        try:
            sidebar_root.update_idletasks()
            sidebar_root.update()
        except Exception:
            sidebar_root = None

    hud_lines = []
    hud_color = (40, 40, 40)
    if current_gesture and (time.time() - gesture_display_time < 1.0):
        gesture_color = GESTURE_COLORS.get(current_gesture, (255, 255, 255))
        hud_lines.append((current_gesture.replace("_", " "), gesture_color))
    hud_lines.append((f"FPS: {fps}", (220, 220, 220)))

    padding = 10
    line_height = 26
    box_width = 0
    for text, _ in hud_lines:
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        box_width = max(box_width, tw)
    box_width += padding * 2
    box_height = len(hud_lines) * line_height + padding * 2
    box_x = 10
    box_y = h - box_height - 10

    cv2.rectangle(frame, (box_x, box_y),
                  (box_x + box_width, box_y + box_height), hud_color, -1)
    cv2.rectangle(frame, (box_x, box_y),
                  (box_x + box_width, box_y + box_height), (255, 255, 255), 1)

    for i, (text, color) in enumerate(hud_lines):
        y = box_y + padding + (i + 1) * line_height - 6
        cv2.putText(frame, text, (box_x + padding, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    target_h = camera_height
    target_w = int(frame.shape[1] * (camera_height / frame.shape[0]))
    if target_w > camera_width:
        target_w = camera_width
        target_h = int(frame.shape[0] * (camera_width / frame.shape[1]))

    frame_resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

    window_w = camera_width
    window_h = camera_height
    window_frame = np.full((window_h, window_w, 3), (18, 18, 18), dtype=np.uint8)
    x = (window_w - target_w) // 2
    y = (window_h - target_h) // 2
    window_frame[y:y+target_h, x:x+target_w] = frame_resized

    cv2.imshow(WINDOW_NAME, window_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()