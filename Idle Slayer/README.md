# Prerequisites for Game Automation Script

## Requirements
Before running the Game Automation script, ensure you have the following dependencies installed:

### 1. Python Version
- Python 3.8 or later is required.

### 2. Required Libraries
Install the following Python libraries using `pip`:
```bash
pip install opencv-python torch numpy pyautogui pygetwindow keyboard ultralytics pillow
```

### 3. YOLOv8 Model
- Ensure you have a trained YOLOv8 model file (`best.pt`).
- If you haven't trained a model, refer to [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/) for guidance.

### 4. Window Title
- The script requires the window title of the target application/game. Ensure you specify the correct title when initializing the script.

### 5. Additional Dependencies
- The script uses `pyautogui` for automation, which requires:
  - A screen display (won't work in a headless environment like some remote servers).
  - Accessibility permissions on macOS.

### 6. Run the Script
Once all dependencies are installed, run the script with:
```bash
python runbot.py
```

### 7. Hotkeys
- Press `q` to manually pause/resume automation.
- The script automatically pauses when the active window changes.

## Troubleshooting
- If you encounter issues detecting the window, ensure the game is running and visible.
- If `pyautogui` interactions do not work, check your OS security settings for automation permissions.

For further assistance, refer to the respective library documentation or open an issue on the project repository.

