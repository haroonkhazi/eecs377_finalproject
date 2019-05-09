from imutils.video import VideoStream
from imutils.io import TempFile
import argparse
from datetime import datetime
from datetime import date
import imutils
import time
import cv2
import os
import numpy as np
import upload



PIN_R = 19
PIN_G = 26
PIN_B = 13
PINS = [PIN_R, PIN_G, PIN_B]
PWM_RANGE = 1000
PWM_FREQUENCY = 1000
NUM = 0

def capture_frame(num):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('webm')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter('/home/pi/eecs377_finalproject/videos/{}.mp4'.format(
                        start_time.strftime("%A_%d_%B_%Y_%I:%M:%S%p_video")),
                        fourcc, 30, (frame_width,frame_height))
    endtime = time.time() + 10
    while time.time() < endtime:
        ret, frame = cap.read()
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.putText(frame, "Room Status: occupied", (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        out.write(frame)
    cap.release()
    out.release()

def setup():
    pi = pigpio.pi()
    for pin in PINS:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)
        pi.set_PWM_frequency(pin, PWM_FREQUENCY)
        pi.set_PWM_range(pin, PWM_RANGE)
        pi.set_PWM_dutycycle(pin, 0)
    return pi


def main():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    minarea=500
    first_frame=None
    occupied = False
    video_recorded = False
    writer = None
    frame_width = None
    frame_height = None
    while True:
        frame = vs.read()
        occupied_prev = occupied
        if frame is None:
            break
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        if frame_width is None or frame_height is None:
            (frame_height, frame_width) = frame.shape[:2]

        mean = np.mean(gray)

        occupied = mean > 50

        if occupied and not occupied_prev:
            start_time = datetime.now()
            writer = cv2.VideoWriter('/Users/haroonkhazi/Desktop/EECS377/final_project/videos/{}.mp4'.format(
                                        start_time.strftime("%A_%d_%B_%Y_%I:%M:%S%p_video")),
                                        0x31637661,25, (500,500))
        elif occupied_prev:
            time_diff = (datetime.now() - start_time).seconds
            if occupied and time_diff > 45:
                if not video_recorded:
                    writer.release()
                    writer = None
                    video_recorded = True
            elif not occupied:
                if video_recorded:
                    video_recorded = False
                else:
                    end_time = datetime.now()
                    total_seconds = (end_time - start_time).seconds
                    writer.release()
                    writer = None
        if writer is not None:
            writer.write(frame)
        cv2.imshow("sss", frame)
        #cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    if writer is not None:
        writer.release()
    vs.stop()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
