import cv2
import mediapipe as mp
import time
import pygame
import json
import tkinter as tk
from threading import Thread

# ---------------- MEDIA PIPE ----------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ---------------- AUDIO / VIDEO ----------------
pygame.mixer.init()

alarm_playing = False
video_cap = None

# ---------------- STATS ----------------
distraction_count = 0
focus_start = time.time()
total_focus_time = 0
distracted_start = None


# ---------------- LOAD / SAVE ----------------
def save_stats():
    data = {
        "distractions": distraction_count,
        "focus_time_sec": int(total_focus_time)
    }

    with open("stats.json", "w") as f:
        json.dump(data, f)


def load_stats():
    global distraction_count, total_focus_time

    try:
        with open("stats.json", "r") as f:
            data = json.load(f)

        distraction_count = data.get("distractions", 0)
        total_focus_time = data.get("focus_time_sec", 0)

    except:
        distraction_count = 0
        total_focus_time = 0


# ---------------- ALARM ----------------
def start_alarm():
    global alarm_playing, video_cap

    if not alarm_playing:

        pygame.mixer.music.load("assets/alarm.mp3")
        pygame.mixer.music.play(-1)

        video_cap = cv2.VideoCapture("assets/alarm.mp4")

        alarm_playing = True


def stop_alarm():
    global alarm_playing, video_cap

    pygame.mixer.music.stop()

    if video_cap is not None:
        video_cap.release()
        video_cap = None

    try:
        cv2.destroyWindow("ALERT")
    except:
        pass

    alarm_playing = False


# ---------------- AI LOGIC ----------------
def run_detector():

    global distraction_count
    global total_focus_time
    global focus_start
    global distracted_start
    global alarm_playing
    global video_cap

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    load_stats()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb)

        status = "NO FACE"
        color = (255, 255, 255)

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]

            nose = face.landmark[1]

            # Looking at screen
            if nose.y < 0.65:

                status = "FOCUSED"
                color = (0, 255, 0)

                distracted_start = None

                total_focus_time += time.time() - focus_start
                focus_start = time.time()

                if alarm_playing:
                    stop_alarm()
                    distraction_count += 1

            # Looking down / distracted
            else:

                status = "DISTRACTED"
                color = (0, 0, 255)

                if distracted_start is None:
                    distracted_start = time.time()

                away_time = time.time() - distracted_start

                if away_time > 2 and not alarm_playing:
                    start_alarm()

                if away_time > 5:
                    cv2.putText(
                        frame,
                        "GET BACK TO WORK!",
                        (20, 250),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

            cv2.putText(
                frame,
                status,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                3
            )

        cv2.putText(
            frame,
            f"Distractions: {distraction_count}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Focus Time: {int(total_focus_time)} sec",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("AI Productivity Tracker", frame)

        # ---------------- ALERT VIDEO ----------------
        if alarm_playing and video_cap is not None:

            ret_video, video_frame = video_cap.read()

            if ret_video:

                video_frame = cv2.resize(video_frame, (640, 360))

                cv2.imshow("ALERT", video_frame)

            else:
                video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    save_stats()

    stop_alarm()

    cap.release()

    cv2.destroyAllWindows()


# ---------------- UI ----------------
def start_app():
    Thread(target=run_detector).start()


def reset_stats():

    global distraction_count
    global total_focus_time

    distraction_count = 0
    total_focus_time = 0

    save_stats()


root = tk.Tk()

root.title("AI Productivity Tracker")

root.geometry("300x200")

btn1 = tk.Button(
    root,
    text="Start Tracking",
    command=start_app,
    height=2,
    width=20
)

btn1.pack(pady=10)

btn2 = tk.Button(
    root,
    text="Reset Stats",
    command=reset_stats,
    height=2,
    width=20
)

btn2.pack(pady=10)

btn3 = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    height=2,
    width=20
)

btn3.pack(pady=10)

root.mainloop()
