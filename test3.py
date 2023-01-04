import time
import wave
import threading
import cv2
import numpy
import pyaudio
from PIL import ImageGrab
from moviepy.editor import *

flag = True
frames = []
frame_count = 0
fps = 24
fourcc = cv2.VideoWriter_fourcc(*'mp4v')


def find_device_index(p):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['name'].find("stereo mix") >= 0 and info['hostApi'] == 0:  # There are characters in the string other than "Stereo Mix"
            return i
    else:
        return -1


def recoder():
    frame = []
    chunks = 1024
    p = pyaudio.PyAudio()
    index = find_device_index(p)
    stream = p.open(input_device_index=index, format=pyaudio.paInt16,
                    channels=2, rate=44100, input=True, frames_per_buffer=chunks)
    while flag:
        data = stream.read(chunks)
        frame.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    return frame



def write_tmp_audio(frames,path="output.wav"):
    p = pyaudio.PyAudio()

    audio = wave.open(path, 'wb')
    # Set audio parameters
    audio.setnchannels(2)
    audio.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    audio.setframerate(44100)
    audio.writeframes(b''.join(frames))  # b" "The prefix means: the following string is of type bytes。
    print("Audio production complete\n")

    audio.close()
    p.terminate()


def is_end():
    while 1:
        tmp = input()
        if tmp == 's':
            global flag
            flag = False
            break


def run_recorder():
    path = "tmp.wav"
    print("start recording\n")
    print("Type s to end recording：")
    frames = recoder()
    write_tmp_audio(frames, path)


def get_screen_size():
    im = ImageGrab.grab()
    return im.size


screen_size = get_screen_size()


def record_screen():
    global frame_count, frames, fps, flag

    count = 0
    begin = time.perf_counter()
    while flag:
        im = ImageGrab.grab()
        frames.append(im)
        count += 1
        frame_count += 1
    end = time.perf_counter()
    fps = count / (end - begin)
    print("fps: ", fps)
    print("screen capture complete\n")
    return fps


def write_silent():
    global frames, frame_count, flag
    out = cv2.VideoWriter("tmp_silent.avi", fourcc, 24, screen_size)
    while flag:
        while frame_count:
            im_cv2 = cv2.cvtColor(numpy.asarray(frames[0]), cv2.COLOR_RGB2BGR)  # convert PIL image to cv2 image
            out.write(im_cv2)
            del (frames[0])
            frame_count -= 1
    out.release()


def reform_silent():
    global fps
    out = cv2.VideoWriter("silent.avi", fourcc, fps, screen_size)
    cap = cv2.VideoCapture("tmp_silent.avi")
    is_success, frame = cap.read()
    count = 0
    while is_success:
        count += 1
        out.write(frame)
        is_success, frame = cap.read()
    print("reform", count, "frames")
    out.release()


def combine_VideoAudio():
    # Combine audio and video
    video = VideoFileClip("silent.avi")
    audio_clip = AudioFileClip('tmp.wav')
    video = video.set_audio(audio_clip)
    video.write_videofile("output.mp4")

    # delet temporary files
    if os.path.exists("tmp.wav"):
        os.remove("tmp.wav")

    if os.path.exists("silent.avi"):
        os.remove("silent.avi")

    if os.path.exists("tmp_silent.avi"):
        os.remove("tmp_silent.avi")


if __name__ == "__main__":
    t1 = threading.Thread(target=is_end)
    t1.setDaemon(True)
    t2 = threading.Thread(target=record_screen)
    t3 = threading.Thread(target=write_silent)
    t4 = threading.Thread(target=run_recorder)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t3.join()

    reform_silent()
    combine_VideoAudio()



