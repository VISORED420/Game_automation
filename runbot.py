import cv2
import torch
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import threading
import keyboard
from ultralytics import YOLO
import PIL.ImageGrab

class GameAutomation:
    def __init__(self, model_path='best.pt', window_title=None):
        """
        Initialize the game automation script with YOLOv8 object detection
        
        :param model_path: Path to the YOLOv8 model weights
        :param window_title: Title of the target window
        """
        # Load YOLOv8 model
        self.model = YOLO(model_path)
        
        # Detection configuration
        self.confidence_threshold = 0.6
        
        # Window targeting
        self.target_window = None
        self.window_title = window_title
        if window_title:
            self.set_target_window(window_title)
        
        # Track previously active window
        self.previous_active_window = None
        
        # Automation control flags
        self.is_running = True
        self.is_paused = False
        
        # Portal detection status
        self.portal_detected = False
        
        # Interaction classes (customize based on your model's classes)
        self.interaction_classes = {
            'closed_chest': self.interact_chest,
            'closed_sp_chest': self.interact_chest,
            'activate_btn': self.interact_activate_button,
            'closed_grey_chest': self.interact_grey_chest,
            'close_btn': self.interact_close_button,
            'left_arrow': self.drag_left_arrow,
            'right_arrow': self.drag_right_arrow
        }

    def set_target_window(self, window_title):
        """
        Set the target window by title
        :param window_title: Title of the window to target
        """
        try:
            # Find the window by title
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                print(f"No window found with title: {window_title}")
                self.target_window = None
                return False
            
            # Take the first matching window
            self.target_window = windows[0]
            self.window_title = window_title
            
            # Activate and bring to foreground
            self.target_window.activate()
            return True
        except Exception as e:
            print(f"Error setting target window: {e}")
            self.target_window = None
            return False

    def check_window_active(self):
        """
        Check if the target window is still active/focused
        
        :return: True if target window is active, False otherwise
        """
        try:
            active_window = gw.getActiveWindow()
            if not active_window or active_window.title != self.window_title:
                if not self.is_paused:
                    print(f"Window changed: {active_window.title if active_window else 'None'}")
                    self.is_paused = True
                return False
            
            # If we were paused due to window change and now we're back to target window
            if self.is_paused and self.previous_active_window != active_window.title:
                print(f"Returned to target window: {self.window_title}")
                self.is_paused = False
            
            # Update previous active window
            self.previous_active_window = active_window.title
            return True
        except Exception as e:
            print(f"Error checking active window: {e}")
            return False

    def capture_window(self):
        """
        Capture the target window
        
        :return: Screenshot of the target window as numpy array
        """
        if not self.target_window:
            raise ValueError("No target window set")
        
        # Get window coordinates
        x, y = self.target_window.topleft
        width = self.target_window.width
        height = self.target_window.height
        
        # Capture specific region
        screenshot = PIL.ImageGrab.grab(bbox=(x, y, x+width, y+height))
        
        # Convert to numpy array
        screenshot_np = np.array(screenshot)
        
        # Convert from RGB to BGR (OpenCV uses BGR)
        return cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    def detect_objects(self, screenshot):
        """
        Detect objects using YOLOv8
        
        :param screenshot: Screen capture
        :return: List of detected objects
        """
        results = self.model(screenshot, conf=self.confidence_threshold)
        
        # Reset portal detection status
        self.portal_detected = False
        
        # Process detections
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class and confidence
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.model.names[cls]
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x, y = (x1 + x2) / 2, (y1 + y2) / 2
                
                detections.append({
                    'class': class_name,
                    'confidence': conf,
                    'center_x': float(x),
                    'center_y': float(y)
                })
        
        return detections

    def interact_chest(self, detection):
        """
        Interaction for chests: click on center
        """
        if self.target_window:
            x, y = self.target_window.topleft
            pyautogui.click(x + detection['center_x'], y + detection['center_y'])
            time.sleep(0.2)

    def interact_activate_button(self, detection):
        """
        Interaction for activate button: click
        """
        if self.target_window:
            x, y = self.target_window.topleft
            pyautogui.click(x + detection['center_x'], y + detection['center_y'])
            time.sleep(0.2)

    def interact_grey_chest(self, detection):
        """
        Interaction for grey chest: click close button
        """
        if self.target_window:
            x, y = self.target_window.topleft
            pyautogui.click(x + detection['center_x'], y + detection['center_y'])
            time.sleep(0.2)

    def interact_close_button(self, detection):
        """
        Interaction for close button: click
        """
        if self.target_window:
            x, y = self.target_window.topleft
            pyautogui.click(x + detection['center_x'], y + detection['center_y'])
            time.sleep(0.2)

    def drag_left_arrow(self, detection):
        """
        Interaction for left arrow: drag to the left edge of the window
        """
        if not self.target_window:
            return
            
        # Get window coordinates
        win_x, win_y = self.target_window.topleft
        
        # Calculate start position (center of the arrow)
        start_x = win_x + detection['center_x']
        start_y = win_y + detection['center_y']
        
        # Calculate end position (left edge of window with small margin)
        end_x = win_x + 5  # 5 pixel margin from left edge
        end_y = start_y  # Keep the same y-coordinate
        
        # Perform the drag operation
        print(f"Dragging left_arrow from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        time.sleep(0.1)  # Small delay to ensure mouse down is registered
        pyautogui.moveTo(end_x, end_y, duration=0.3)  # Smooth drag
        time.sleep(0.1)  # Small delay before releasing
        pyautogui.mouseUp()
        
        # Wait a bit after the action
        time.sleep(0.5)

    def drag_right_arrow(self, detection):
        """
        Interaction for right arrow: drag to the right edge of the window
        """
        if not self.target_window:
            return
            
        # Get window coordinates
        win_x, win_y = self.target_window.topleft
        win_width = self.target_window.width
        
        # Calculate start position (center of the arrow)
        start_x = win_x + detection['center_x']
        start_y = win_y + detection['center_y']
        
        # Calculate end position (right edge of window with small margin)
        end_x = win_x + win_width - 5  # 5 pixel margin from right edge
        end_y = start_y  # Keep the same y-coordinate
        
        # Perform the drag operation
        print(f"Dragging right_arrow from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        time.sleep(0.1)  # Small delay to ensure mouse down is registered
        pyautogui.moveTo(end_x, end_y, duration=0.3)  # Smooth drag
        time.sleep(0.1)  # Small delay before releasing
        pyautogui.mouseUp()
        
        # Wait a bit after the action
        time.sleep(0.5)

    def run_automation(self):
        """
        Main automation loop
        """
        if not self.target_window:
            print("No target window set. Use set_target_window() first.")
            return
        
        # Set up keyboard listener for pausing
        keyboard.add_hotkey('q', self.toggle_manual_pause)
        print("Press 'q' to manually pause/resume automation")
        print("Automation will automatically pause when window focus changes")
        
        try:
            while self.is_running:
                # Check if window is still active
                self.check_window_active()
                
                # Pause if paused
                if self.is_paused:
                    time.sleep(0.5)
                    continue
                
                # Capture window
                try:
                    screenshot = self.capture_window()
                except Exception as e:
                    print(f"Error capturing window: {e}")
                    # Try to re-acquire the window
                    if not self.set_target_window(self.window_title):
                        time.sleep(1)
                        continue
                
                # Detect objects
                detections = self.detect_objects(screenshot)
                
                # Process detections for interactions
                for detection in detections:
                    if detection['class'] in self.interaction_classes:
                        # Call corresponding interaction method
                        interaction_method = self.interaction_classes[detection['class']]
                        interaction_method(detection)
                
                # Polling interval
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            self.cleanup()
            print("Automation stopped.")

    def toggle_manual_pause(self):
        """
        Toggle manual pause state of the automation
        """
        self.is_paused = not self.is_paused
        status = "PAUSED" if self.is_paused else "RESUMED"
        print(f"Automation manually {status}")

    def cleanup(self):
        """
        Clean up resources and stop threads
        """
        self.is_running = False
        keyboard.unhook_all()

def main():
    # Usage example - replace with your actual window title
    game_automation = GameAutomation(
        model_path='best.pt',
        window_title="Idle Slayer"
    )
    game_automation.run_automation()

if __name__ == "__main__":
    main()