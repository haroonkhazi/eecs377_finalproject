import numpy as np
import cv2
from imutils.video import VideoStream
import datetime
import imutils
import time


cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('outpy.avi',fourcc, 10, (frame_width,frame_height))
firstFrame = None
while(cap.isOpened()):
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    stream_frame = vs.read()
    capture_frame = cap.read()
    text = "Unoccupied"
    if capture_frame is None or stream_frame is None:
        break

    stream_frame = imutils.resize(stream_frame, width=500)
    gray = cv2.cvtColor(stream_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    num = 0
    for c in cnts:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        if cv2.contourArea(c) < args["min_area"]:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(stream_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            out = cv2.VideoWriter('{}_video.avi'.format(num),fourcc, 10, (frame_width,frame_height))
            out.write(capture_frame)
            text = "Occupied"
        num = num + 1

    cv2.putText(stream_frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(stream_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, stream_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", stream_frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
