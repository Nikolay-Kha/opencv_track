#!/usr/bin/env python

import argparse
import datetime
import imutils
import os
import time
import cv2
import tracking_object
import color_detector

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
fps_time = time.time()
fps = 0

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
        try:
            obj.update(frame)
        except cv2.error:
            tracking_objs.remove(obj)
            print("Delete tracker due to the error")
            break
        if obj.ts <= 0:
            tracking_objs.remove(obj)
            print("Delete tracker")

    # Detect people in the image
    if frame_number % 10 == 0:
        found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.02)

        for (x, y, w, h) in found:
            intersects = False
            for obj in list(tracking_objs):
                if obj.intersect_area(x, y, w, h) > 0.5 * obj.area():
                    intersects = True
                    obj.update_ts()

            if not intersects:
                img = frame[y:y + h, x:x + w]
                s = ""
                d = color_detector.detect(img)
                if d is not None:
                    dx, dy, dw, dh = d
                    s = "-DETECTED"
                    cv2.rectangle(img, (dx, dy), (dx + dw, dy + dh), (0, 255, 0), 2)
                name = datetime.datetime.now().strftime("img/%Y-%m-%d_%H:%M:%S_{}{}.jpg".format(img_num, s))
                img_num += 1
                print("Saving " + name)
                cv2.imwrite(name, img)
                tracking_obj = tracking_object.TrackingObject(frame, x, y, w, h)
                tracking_objs.append(tracking_obj)
                print("Create tracker: " + str(tracking_obj))

    # Draw results
    for (x, y, w, h) in found:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for o in tracking_objs:
        cv2.rectangle(frame, (o.x, o.y), (o.x + o.w, o.y + o.h), (0, 0, 255), 2)
    ct = time.time()
    fps = fps * 0.9 + (1.0 / (ct - fps_time)) * 0.1
    fps_time = ct
    cv2.putText(frame, "FPS is " + str(round(fps, 1)), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

    cv2.imshow("Detector", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    frame_number += 1

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
