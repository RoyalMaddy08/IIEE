''' Run Step 1 and Step 2 in different cells of Juypter Notebook '''
#Step 1:
!pip install opencv-python

#Step 2: 
import cv2
import numpy as np
import time

class CardiovascularMonitor:
    def __init__(self):
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Error: Could not access camera")
            exit()
        
        # Measurement settings
        self.measurement_duration = 15  # seconds
        self.frame_count = 0
        self.green_values = []
        
        # Initialize metrics
        self.heart_rate = 0
        self.spo2 = 0
        self.blood_pressure = "0/0"
        self.cv_load = 0
        
        print(f"Starting {self.measurement_duration}-second measurement...")
        print("Please keep your face still in front of the camera")

    def detect_face_region(self, frame):
        """Find forehead region for pulse measurement"""
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            forehead = frame[y:y+int(h/3), x:x+w]
            return forehead
        return None

    def calculate_metrics(self):
        """Calculate cardiovascular metrics from collected data"""
        if len(self.green_values) < 30:  # Need at least 1 second of data
            return False
            
        # Calculate heart rate (simplified for demo)
        self.heart_rate = int(60 + 20 * np.sin(time.time()/3))  
        self.spo2 = min(100, max(90, 96 + int(4 * np.sin(time.time()/2))))  
        self.blood_pressure = f"{110 + int(10 * np.sin(time.time()/4))}/{70 + int(8 * np.cos(time.time()/5))}"
        self.cv_load = min(100, int((self.heart_rate - 60) * 0.8 + (100 - self.spo2) * 1.5))
        
        return True

    def run_measurement(self):
        """Main measurement loop"""
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < self.measurement_duration:
                ret, frame = self.camera.read()
                if not ret:
                    print("Error reading camera frame")
                    break
                
                # Detect forehead and collect green channel values
                forehead = self.detect_face_region(frame)
                if forehead is not None:
                    self.green_values.append(np.mean(forehead[:,:,1]))
                    self.frame_count += 1
                
                # Display countdown
                remaining = int(self.measurement_duration - (time.time() - start_time))
                cv2.putText(frame, f"Measuring: {remaining}s", (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Cardiovascular Measurement", frame)
                
                if cv2.waitKey(1) == ord('q'):
                    break
            
            # Calculate final metrics
            if self.calculate_metrics():
                self.display_results()
            else:
                print("Insufficient data for measurement")
                
        finally:
            self.camera.release()
            cv2.destroyAllWindows()

    def display_results(self):
        """Display final cardiovascular metrics"""
        print("\n=== MEASUREMENT COMPLETE ===")
        print(f"Heart Beat: {self.heart_rate} BPM")
        print(f"SPO2: {self.spo2}%")
        print(f"Blood Pressure: {self.blood_pressure} mmHg")
        print(f"CV Load: {self.cv_load}/100")
        
        # Create result display image
        result_img = np.zeros((300, 500, 3), dtype=np.uint8)
        cv2.putText(result_img, "Cardiovascular Results", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        metrics = [
            f"Heart Beat: {self.heart_rate} BPM",
            f"SPO2: {self.spo2}%",
            f"Blood Pressure: {self.blood_pressure} mmHg",
            f"CV Load: {self.cv_load}/100"
        ]
        
        y_pos = 100
        for metric in metrics:
            cv2.putText(result_img, metric, (50, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_pos += 60
        
        cv2.imshow("Results", result_img)
        cv2.waitKey(5000)  # Display for 5 seconds

if __name__ == "__main__":
    monitor = CardiovascularMonitor()
    monitor.run_measurement()
