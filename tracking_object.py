import cv2
import time
import math

class TrackingObject:

    def __init__(self, frame, x, y, w, h):
        # MIL is better, KCF is worse but faster
        self.obj = cv2.Tracker_create("KCF")
        self.obj.init(frame, (x, y, w, h))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.origin_center_x = x + w / 2
        self.origin_center_y = y + h / 2
        self.mx = 0
        self.my = 0
        self.mw = 0
        self.mh = 0
        self.mimg = None
        self.ts = 0
        self.update_ts()

    def update_ts(self):
        self.ts = 30

    def update(self, frame):
        ok, bbox = self.obj.update(frame)
        self.x = int(bbox[0])
        self.y = int(bbox[1])
        self.w = int(bbox[2])
        self.h = int(bbox[3])

    def is_intersects(self, x, y, w, h):
        if x + w < self.x:
            return False
        if self.x + self.w < x:
            return False
        if y + h < self.y:
            return False
        if self.y + self.h < y:
            return False
        return True

    def walked_distance(self):
        x = self.x + self.w / 2 - self.origin_center_x
        y = self.y + self.h / 2 - self.origin_center_y
        return math.sqrt(x * x + y * y)

    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y) + ', w: ' + str(self.w) + ', h: ' + str(self.h) + ', ts: ' + str(self.ts)

    def _get_bound(self):
        return self.x, self.x + self.w, self.y, self.y + self.h

    def expand(self, frame, mo):
        (l, r, t, b) = self._get_bound()
        (ml, mr, mt, mb) = mo._get_bound()
        if ml < l:
            l = ml
        if mr > r:
            r = mr
        if mt < t:
            t = mt
        if mb > b:
            b = mb
        self.x = l
        self.y = t
        self.w = r - l
        self.h = b - t
        self.obj = cv2.Tracker_create("MIL")
        self.obj.init(frame, (self.x, self.y, self.w, self.h))

