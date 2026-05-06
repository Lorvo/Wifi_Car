import socket
import cv2
import time
import numpy as np
from picamera2 import Picamera2
import pigpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)

servoCtl = GPIO.PWM(7, 50)
speedCtl = GPIO.PWM(33, 500)
servoCtl.start(0)
speedCtl.start(0)

width = 640
height = 480
oldServo = 7.5
prevServo = 7.5
piCam = Picamera2()
piCam.preview_configuration.main.size = (width, height)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

bufferSize = 30000
serverPort = 2222
serverIP = "192.168.1.241"
quality = 40
dt = .03
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
RPIsocket.bind((serverIP, serverPort))
RPIsocket.listen()

try:
        while True:
                print("waiting for client")
                client, address = RPIsocket.accept()
                print("client connected>>> ", address)
                while True:
                        try:
                                message = client.recv(512).decode("utf-8")
                                data = message.split(',')
                                if len(data) > 2:
                                        data = [data[0], data[-1]]
                                if (len(data) > 1):
                                        GPIO.output(31, int(data[1]) <= 0)
                                        GPIO.output(29, int(data[1]) > 0)
                                        speedCtl.ChangeDutyCycle(abs(int(data[1])))

                                        #######################################################################################
                                        ######### Implementing a low-pass filter to reduce servo jitter doesn't help ##########
                                        ######### because the problem is inconsistent Rpi timing (perhaps)           ##########
                                        #######################################################################################

                                        #newServo = float(data[0]) * .2 + prevServo * .8
                                        #prevServo = newServo
                                        #print(round(newServo, 4))
                                        #if (round(newServo, 2) != round(oldServo, 2)):
                                        #       servoCtl.ChangeDutyCycle(round(newServo, 2))
                                        #       oldServo = newServo
                                        #else:
                                        #       servoCtl.ChangeDutyCycle(0)
                                        #if (newServo < 5.84 or newServo > 9.16):
                                        #       servoCtl.ChangeDutyCycle(0)



                                        if round(float(data[0]), 2) != oldServo:
                                                servoCtl.ChangeDutyCycle(round(float(data[0]), 2))
                                                oldServo = round(float(data[0]), 2)
                                        else:
                                                servoCtl.ChangeDutyCycle(0)
                                frame = piCam.capture_array()
                                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                                ret, buffer = cv2.imencode('.jpeg', frame, encode_param)
                                frame = buffer.tobytes()
                                client.sendall(frame)
                                #time.sleep(dt)

                        except Exception as e:
                                print(e)
                                print("client disconnected")
                                client.close()
                                break


except KeyboardInterrupt:
        GPIO.cleanup()
        speedCtl.stop(0)
        client.close()



