from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
import os
import cv2



ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", help="name of file to save")
args = vars(ap.parse_args())
name = args["name"]
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
t_end = time.time() + 60 * 2
while time.time() < t_end:
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)
    else:
      break
cap.release()
out.release()
