import numpy as np
import cv2
import time
import queue
from threading import Thread

class CardiovascularMonitor:
    def __init__(self, video_source=0):
        # Initialize camera
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open video source")
           
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
       
        # Initialize measurements
        self.current_bpm = 72
        self.current_spo2 = 98
        self.current_hrv = 50
        self.systolic_bp = 120
        self.diastolic_bp = 80
        self.cardiovascular_load = 30
       
        # Create window
        cv2.namedWindow("Cardiovascular Monitor", cv2.WINDOW_NORMAL)
       
        # Start processing thread
        self.processing_queue = queue.Queue(maxsize=1)
        self.running = True
        self.processing_thread = Thread(target=self.process_frames)
        self.processing_thread.start()

    def process_frames(self):
        """Thread for processing frames"""
        while self.running:
            try:
                # Get frame from queue
                frame = self.processing_queue.get(timeout=0.1)
               
                # Simulate processing (replace with actual processing)
                time.sleep(0.02)  # Simulate 20ms processing time
               
            except queue.Empty:
                continue

    def update_display(self, frame):
        """Update the display with measurements"""
        # Create overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (400, 220), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
       
        # Display measurements with colored indicators
        y_pos = 60
        cv2.putText(frame, "Cardiovascular Monitor", (30, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
       
        metrics = [
            (f"Heart Rate: {self.current_bpm} BPM", self.get_bpm_color()),
            (f"SpO2: {self.current_spo2}%", self.get_spo2_color()),
            (f"HRV: {self.current_hrv} ms", self.get_hrv_color()),
            (f"Blood Pressure: {self.systolic_bp}/{self.diastolic_bp} mmHg", self.get_bp_color()),
            (f"CV Load: {self.cardiovascular_load}", self.get_load_color())
        ]
       
        for text, color in metrics:
            cv2.putText(frame, text, (30, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_pos += 40

    def get_bpm_color(self):
        if self.current_bpm > 100: return (0, 0, 255)    # Red
        elif self.current_bpm < 60: return (0, 165, 255)  # Orange
        return (0, 255, 0)                               # Green

    def get_spo2_color(self):
        return (0, 0, 255) if self.current_spo2 < 95 else (0, 255, 0)

    def get_hrv_color(self):
        return (0, 0, 255) if self.current_hrv < 30 else (0, 255, 0)

    def get_bp_color(self):
        if self.systolic_bp > 140 or self.diastolic_bp > 90: return (0, 0, 255)
        return (0, 255, 0)

    def get_load_color(self):
        if self.cardiovascular_load > 80: return (0, 0, 255)
        elif self.cardiovascular_load > 60: return (0, 165, 255)
        elif self.cardiovascular_load > 40: return (0, 255, 255)
        return (0, 255, 0)

    def run(self):
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to capture frame")
                    break
               
                # Send frame to processing thread
                try:
                    self.processing_queue.put_nowait(frame.copy())
                except queue.Full:
                    pass
               
                # Update display
                self.update_display(frame)
               
                # Show frame
                cv2.imshow("Cardiovascular Monitor", frame)
               
                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                   
        finally:
            self.running = False
            self.processing_thread.join()
            self.cap.release()
            cv2.destroyAllWindows()
            print("Monitor stopped")

if __name__ == "__main__":
    print("Starting Cardiovascular Monitor...")
    monitor = CardiovascularMonitor()
    monitor.run()
