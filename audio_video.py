import datetime
import time
from PIL import ImageGrab
import sounddevice
import numpy as np
import cv2
from win32api import GetSystemMetrics
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import moviepy.editor as mpe
import pyautogui
import ffmpeg
from moviepy.editor import *
import os

# store starting time
begin = time.time()
resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"MPEG")
time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename1 = f'{time_stamp}.avi'

# Specify frames rate. We can choose any
 # value and experiment with it
fps = 20.0

# Creating a VideoWriter object
out = cv2.VideoWriter(filename1, codec, fps, resolution)

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
    if cv2.waitKey(10) == ord('q'):
        time.sleep(1)
        # store end time
        end = time.time()
        break

# Release the Video writer
out.release()

# Destroy all windows
cv2.destroyAllWindows()
time_taken1 = end - begin
print("Screen recording completed")
print(time_taken1)



# voice recoder

# def voice_recoder():
begin2 = time.time()
fs = 44100
second = time_taken1
print("Recording.....n")
record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
sounddevice.wait()
time_stamp2 = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename2 = f'{time_stamp2}.wav'
out2 = write(filename2, fs, record_voice)
print("Finished.....nPlease check your output file")
time.sleep(1)
# store end time
end2 = time.time()
time_taken2 = end2 - begin2
print("voice recording completed")
if time_taken2 == time_taken1:
    exit()

# loading video dsa gfg intro video
clip = VideoFileClip(f'{time_stamp}.avi')


# getting only first 5 seconds
clip = clip.subclip(0, time_taken2)

# loading audio file
audioclip = AudioFileClip(f'{time_stamp2}.wav').subclip(0, time_taken2)

# adding audio to the video clip
videoclip = clip.set_audio(audioclip)

# showing video clip
# codec3 = cv2.VideoWriter_fourcc(*"MPEG")
time_stamp3 = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename3 = f'{time_stamp3}.avi'
out3 =videoclip.write_videofile(filename3,"MPEG")

exit()




