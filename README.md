# Cardiovascular Monitor 🩺📷

A real-time cardiovascular monitoring system using a standard webcam and OpenCV.

This project extracts physiological signals from facial video — specifically the green channel intensity of the forehead region — to estimate cardiovascular metrics such as:

-  Heart Rate (BPM)  
-  SpO2 (Oxygen Saturation)  
-  Blood Pressure (simulated)  
-  Cardiovascular Load



---

## Features

✅ Face and forehead region detection  
✅ Real-time green channel data extraction  
✅ 15-second data capture and analysis  
✅ Visualization of estimated results (OpenCV window)  
✅ All built with standard libraries — no external devices required

---
How It Works
A webcam feed is accessed using OpenCV.

The system detects the face and focuses on the forehead.

Green channel intensity (related to blood perfusion) is captured frame by frame.

Basic estimations of cardiovascular metrics are made based on the signal pattern.

Final results are displayed after the capture duration.


=== MEASUREMENT COMPLETE ===

Heart Beat: 72 BPM

SpO2: 98%

Blood Pressure: 118/76 mmHg

CV Load: 12/100
