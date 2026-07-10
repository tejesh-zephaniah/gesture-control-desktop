# Gesture Control Desktop

Control your computer using hand gestures through a webcam.

> A Windows executable is available in the `v1.0` release. See the [release page](https://github.com/tejesh-zephaniah/gesture-control-desktop/releases/tag/v1.0).
> The executable runs without installing Python or dependencies.

## Overview

This project uses computer vision to detect hand movements and convert them into system actions.
It supports gesture-driven mouse control, click actions, volume control, screenshots, and a gesture reference overlay.

## Current Status

* Hand detection and landmark extraction are working
* Finger states (up/down) are detected reliably
* Mouse movement, click, mute/unmute, volume control, and screenshot gestures are implemented
* The application includes a sidebar gesture reference and a clean HUD overlay

## Project Structure

```
gesture-control-desktop/
│
├── camera/        # camera handling
├── vision/        # hand detection and landmark processing
├── gestures/      # gesture classification logic
├── controller/    # system actions and input control
├── utils/         # helper functions
├── main.py        # entry point
```

## Setup

```bash
git clone https://github.com/tejesh-zephaniah/gesture-control-desktop
cd gesture-control-desktop

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

## Download

A ready-to-run Windows executable is available in the GitHub Releases page.
Download `gestora-ai.exe` from the `v1.0` release to use the app without installing Python or dependencies.

## What it does right now

* Detects your hand in real-time
* Tracks finger positions and extracts gestures
* Moves mouse cursor using hand position
* Supports left click, mute/unmute, volume control, and screenshot gestures
* Displays a gesture reference sidebar and FPS HUD overlay

## Contributing

Feel free to explore, test, and suggest improvements.
