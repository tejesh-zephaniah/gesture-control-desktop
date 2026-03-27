# Gesture Control Desktop

Control your computer using hand gestures through a webcam.

---

## Overview

This project uses computer vision to detect hand movements and convert them into simple actions.
The goal is to build a system that works across different operating systems (Linux, Windows, macOS).

---

## Current Status

* Hand detection is working
* Landmarks are being extracted
* Finger states (up/down) are detected
* Gesture logic is being developed

---

## Project Structure

```
gesture-control-desktop/
│
├── camera/        # camera handling
├── vision/        # hand detection and landmarks
├── gestures/      # gesture logic (in progress)
├── controller/    # system control (planned)
├── utils/         # helper functions
├── main.py        # entry point
```

---

## Setup

```bash
git clone https://github.com/tejesh-zephaniah/gesture-control-desktop
cd gesture-control-desktop

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

---

## What it does right now

* Detects your hand in real-time
* Tracks finger positions
* Outputs finger states

---

## Planned

* Cursor movement
* Click using gestures
* Volume control
* More gestures

---

## Contributing

This project is still in progress.
Feel free to explore, test, and suggest improvements.

---

## Status

Work in progress.
