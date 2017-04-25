#!/usr/bin/env python

import argparse
import datetime
import imutils
import time
import cv2
import tracking_object
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)
# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])

cv2.namedWindow("Detector");
cv2.moveWindow("Detector", 20,20);

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
frame_number = 0
tracking_objs = []
img_num = 0

try:
    os.mkdir("img")
except OSError:
    for _, _, files in os.walk("img"):
        for name in files:
            os.remove("img/" + name)

while True:
    (grabbed, frame) = camera.read()
    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)

    for obj in list(tracking_objs):
        # if frame_number % 10 == 0:
        obj.ts -= 1
        obj.update(frame)
        if obj.ts <= 0:
            tracking_objs.remove(obj)
            if obj.walked_distance() > 30 and obj.mimg is not None:
                name = datetime.datetime.now().strftime("img/%Y-%m-%d %H:%M:%S {}.jpg".format(img_num))
                print("Delete tracker and saving " + name)
                cv2.imwrite(name, obj.mimg)
                img_num += 1
            else:
                print("Delete tracker, no movement")
            continue

    # Detect people in the image
    if frame_number % 10 == 0:
        found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)

        for (x, y, w, h) in found:
            intersects = False
            for obj in list(tracking_objs):
                if obj.is_intersects(x, y, w, h):
                    # if intersects:
                    #     tracking_objs.remove(obj)
                    #     print("Delete tracker which tracks the same object")
                    #     continue
                    intersects = True
                    obj.update_ts()
                    if w * h > obj.mw * obj.mh:
                        obj.mw = w
                        obj.mh = h
                        obj.mimg = frame[y:y + h, x:x + w].copy()

            if not intersects:
                #height, width, channels = frame.shape
                #cx = x + w / 2
                #cy = y + h / 2
                #if cx > width * 0.1 and cx < width * 0.9 and cy > height * 0.1 and cy < height * 0.9:
                tracking_obj = tracking_object.TrackingObject(frame, x, y, w, h)
                tracking_objs.append(tracking_obj)
                print("Create tracker: " + str(tracking_obj))

    # Draw results
    for (x, y, w, h) in found:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for o in tracking_objs:
        cv2.rectangle(frame, (o.x, o.y), (o.x + o.w, o.y + o.h), (0, 0, 255), 2)

    cv2.imshow("Detector", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    frame_number += 1

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
