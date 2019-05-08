from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import upload

# construct the argument parser and parse the arguments


def capture_frame(num):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter('{}.video.mp4'.format(num),fourcc, 25, (frame_width,frame_height))
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

def main():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    firstFrame = None
    minarea=500
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
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        num = 0
        for c in cnts:
            if cv2.contourArea(c) > minarea:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                img_name = "picture.frame.{}.png".format(num)
                path = '/Users/haroonkhazi/desktop/eecs377/final_project/videos'
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                cv2.imwrite(os.path.join(path , img_name), frame)
                #cv2.imwrite(img_name, frame)
                #capture_frame(num)
                num = num + 1



                # draw the text and timestamp on the frame
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
