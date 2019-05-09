from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import numpy as np
#import pigpio
import upload



PIN_R = 19
PIN_G = 26
PIN_B = 13
PINS = [PIN_R, PIN_G, PIN_B]
PWM_RANGE = 1000
PWM_FREQUENCY = 1000
NUM = 0

def capture_frame():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    start_time = datetime.datetime.now()
    out = cv2.VideoWriter('/Users/haroonkhazi/Desktop/EECS377/final_project/videos/{}.mp4'.format(
                            start_time.strftime("%A_%d_%B_%Y_%I:%M:%S%p_video")),
                            0x31637661, 25, (frame_width,frame_height))
    endtime = time.time() + 10
    while time.time() < endtime:
        ret, frame = cap.read()
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.putText(frame, "Room Status: occupied", (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        out.write(frame)
    cap.release()
    out.release()




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--vid",help="Pictures or Videos to Capture? ")
    args = vars(ap.parse_args())
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    firstFrame = None
    saved_frame=None
    minarea=500
    num = 0
    pic=False
    num=0
    if args.get("vid", None) is None:
        pic=True

    while True:
        frame = vs.read()
        text = "Unoccupied"
        if frame is None:
            break

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            num=0
            continue
        if saved_frame is None:
            saved_frame=gray

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) > minarea:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if num % 10 == 1:
                    saved_frame=gray
                if num % 10 == 0 and num != 0:
                    frame_delta = cv2.absdiff(saved_frame, gray)
                    new_thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                    print(np.sum(new_thresh))
                    if np.sum(new_thresh) > 0:
                        firstFrame = gray
                if pic:
                    start_time = datetime.datetime.now()
                    img_name = "{}.picture.png".format(start_time.strftime("%A_%d_%B_%Y_%I:%M:%S%p_video"))
                    path = '/Users/haroonkhazi/Desktop/EECS377/final_project/videos'
                    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    cv2.imwrite(os.path.join(path , img_name), frame)
                else:
                    capture_frame()
                num=num+1


        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        cv2.imshow("Security Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):

            break

    vs.stop()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
