import cv2
import numpy as np
import json
from datetime import datetime as dt
import subprocess
import time
import pyautogui
import pyautogui as gui
import link
import getpass



username = getpass.getuser()


def getTime():
    with open('timetable.json', 'r') as f:
        timetable = json.load(f)
    return timetable


def checkClass(timetable):
    day = dt.now().strftime("%A").lower()
    schedule = timetable[day]
    while True:
        cTime = dt.now().strftime("%I:%M")
        if cTime in schedule:
            openZoom()
            time.sleep(240)


def openZoom():
    subprocess.Popen(fr"C:\Users\Babu Moshay\AppData\Roaming\Zoom\bin\Zoom.exe")  # Change app location here
    time.sleep(15)
    joinClass()


def buttonClick(image):
    btn = gui.locateCenterOnScreen(image)
    gui.moveTo(btn)
    gui.click()
    time.sleep(2)


def buttonWrite(text):
    gui.write(text)
    time.sleep(1)
    gui.press('enter')


def joinClass():
    buttonClick('images/main-join-btn.png')
    buttonWrite(link.ID)
    time.sleep(6)
    buttonWrite(link.PASS)

resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"XVID")

filename = "venv/Recording.avi"

# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0

# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)

# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 270)

while True:
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    frame = np.array(img)

    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write it to the output file
    out.write(frame)

    # Optional: Display the recording screen
    cv2.imshow('Live', frame)

    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Release the Video writer
out.release()

# Destroy all windows
cv2.destroyAllWindows()


timetable = getTime()
checkClass(timetable)
