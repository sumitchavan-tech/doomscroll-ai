# 🧠 AI Doomscroll Detection System

## 📌 Project Description
This project is a real-time AI-based productivity tracker that detects user distraction using webcam input. It identifies whether the user is focused or distracted and triggers alerts (audio + video) to reduce doomscrolling behavior and improve productivity.

---

## ⚙️ Technologies Used
- Python  
- OpenCV (Computer Vision)  
- MediaPipe (Face Tracking)  
- Pygame (Audio Control)  
- Tkinter (Desktop UI)  
- JSON (Data Storage)  
- PyInstaller (Optional EXE creation)

---

## 🚀 Features
- Real-time face detection using webcam  
- Nose-based attention tracking  
- Detects focused vs distracted state  
- Audio alarm system when distracted  
- Video alert popup  
- Focus time tracking  
- Distraction counter  
- Saves user stats in JSON file  
- Optional graph visualization support  
- Desktop UI (Start / Reset / Exit)

---

## 📊 Working Logic
- If user is looking at screen → Focus mode  
- If user looks away → Distracted mode  
- If distraction continues → Alarm starts  
- When user returns → Alarm stops + counter increases  

---

## 📁 Project Structure

Doomscroolingstop/
│
├── screen_detector_v4.py
├── stats.json
├── assets/
│ ├── alarm.mp3
│ └── alarm.mp4


---

## ▶️ How to Run
```bash
pip install opencv-python mediapipe pygame matplotlib
python screen_detector_v4.py

Project Goal

To reduce digital distraction and improve focus using AI-based real-time monitoring.

Author

Student Project – AI Productivity Tracker System
