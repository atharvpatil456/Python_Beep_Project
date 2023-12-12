import cv2
import pygame
import tkinter as tk

global motion_detection_on
motion_detection_on = False
sound_played = False  

def toggle_motion_detection():
    global motion_detection_on
    motion_detection_on = not motion_detection_on

def exit_app():
    global running
    running = False

cam = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Motion Detection")
root.geometry("400x150")

label = tk.Label(root, text="Click 'Start' to begin motion detection.\nPress 'Q' to stop and exit.")
label.pack()

start_stop_button = tk.Button(root, text="Start", command=toggle_motion_detection)
start_stop_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack()

running = True

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("A:/Python_TA/beep.mp3")  # Provide the correct file path

while running:
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    if motion_detection_on:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        sound_played = False

        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not sound_played:
                pygame.mixer.music.play()
                sound_played = True

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break

    cv2.imshow('Motion Detection', frame1)

    root.update()

cam.release()
cv2.destroyAllWindows()
root.destroy()
