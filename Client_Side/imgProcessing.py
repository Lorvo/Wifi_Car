import numpy as np
import cv2
import pickle
from time import sleep

class Feed:

    def __init__(self, w, h):
        
        with open("settings.pkl", "rb") as f:
            self.data = pickle.load(f)

        self.width = w
        self.height = h
        self.steerVal = 7.5
        self.steerAngle = self.data["angle"]
        self.yVals = np.linspace(0, self.height / 2, 1000)
        self.bend = 0
        self.maxBend = self.data["bend"]
        self.offset = self.data["offset"]
        self.dSlp = self.data["slope"]
        self.bendResolution = 255
        self.fontScale = 2
        self.fontThickness = 5

        cv2.namedWindow('vid')

    def showImg(self, img):
        try:
            cv2.imshow("vid", img)
            cv2.waitKey(1)

        except:
            print(f"[SHOW ERROR]")

    def drawLine(self, canvas):
        overlay = np.zeros_like(canvas, np.uint8)
        cnt = 0
        slp = 0
        for val in self.yVals:
            r = int((-39/1000*cnt) + 40)
            cnt = cnt + 1
            slp = slp + self.dSlp
            cv2.circle(overlay, (int(((val)**2)*self.bend+ self.offset + slp), (int((val))-self.height)*-1), r, (0, 255, 0), -1)
            cv2.circle(overlay, (int(((val)**2)*self.bend+(self.width - self.offset) - slp), (int((val))-self.height)*-1), r, (0, 255, 0), -1)
        alpha = .8
        mask = overlay.astype(bool)
        canvas[mask] = cv2.addWeighted(canvas, alpha, overlay, 1 - alpha, 0)[mask]

    def showEncodedImg(self, bytes, text, textCol):
        try:
            data_encode = np.asarray(bytearray(bytes), dtype="uint8")
            cv2.waitKey(50)
            Jtext_width, Jtext_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            img = cv2.imdecode(data_encode, cv2.IMREAD_COLOR)
            img = cv2.putText(img, text, (5, Jtext_height + 5), cv2.FONT_HERSHEY_SIMPLEX, 1, textCol, 2, cv2.LINE_AA)
            self.drawLine(img)
            cv2.imshow("vid", img)
            cv2.waitKey(1)

        except: #NameError as err:
            pass
            #print(f"[FRAME ERROR] >>> {err}")

    def calculateBend(self, xAxis):
        self.bend = (((self.maxBend*2)/200) * xAxis) - (((self.maxBend*2)/200) * -100) - self.maxBend

    def setOptions(self, mBend, slp, offs, ang):
        self.maxBend = mBend
        self.dSlp = slp
        self.offset = offs
        self.steerAngle = ang