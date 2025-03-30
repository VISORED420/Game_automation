# Game Automation using YOLOv8

## Overview
This repository contains a machine learning-based game automation script utilizing YOLOv8 for real-time object detection. The script automates interactions within a game by detecting UI elements and objects using a pre-trained YOLOv8 model.

## Features
- **Real-time Object Detection**: Uses YOLOv8 to detect key game elements.
- **Automated Interactions**: Clicks buttons, interacts with objects, and performs in-game actions.
- **Window Targeting**: Identifies and focuses on a specific game window.
- **Hotkeys for Control**: Supports manual pausing and resuming.
- **Customizable Actions**: Configure interaction behaviors for detected objects.

## Prerequisites
### **1. Install Dependencies**
Ensure you have Python 3.8 or later and install the required libraries:
```bash
pip install opencv-python torch numpy pyautogui pygetwindow keyboard ultralytics pillow
```

### **2. YOLOv8 Model**
- Place a trained YOLOv8 model file (`best.pt`) in the project directory.
- Train a custom YOLOv8 model if needed by following [Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/).

### **3. Game Window Setup**
- Ensure the target game is running and specify its window title when initializing the script.

## Usage
### **Run the Automation Script**
```bash
python game_automation.py
```
### **Hotkeys**
- Press `q` to pause/resume automation.
- The script automatically pauses when the game window loses focus.

## How It Works
1. Captures the game window in real-time.
2. Runs YOLOv8 to detect predefined objects.
3. Performs automated interactions based on detected objects.
4. Uses `pyautogui` for mouse-based interactions.
5. Continuously checks for window focus to ensure seamless operation.

## Troubleshooting
- **Detection Issues**: Ensure the YOLO model is trained on relevant game elements.
- **Automation Not Working**: Check if the game runs in full-screen mode (windowed mode is recommended).
- **Permission Errors**: On macOS, allow automation permissions for `pyautogui` in system settings.

## Contributing
Feel free to submit pull requests to improve the automation features or add support for more games.

## License
This project is open-source under the MIT License.

