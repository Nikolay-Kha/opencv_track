import cv2

# use range-detector ( https://github.com/jrosebr1/imutils/blob/master/bin/range-detector )
# to choose colors range
# python range-detector -f HSV -i "img/2017-04-28 16:44:30 1.jpg"
colorLower = (0, 120, 120)
colorUpper = (60, 255, 255)


def detect(img):
    height, width, _ = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        if y + h > height * 0.5:
            return None
        return x, y, w, h
    return None
