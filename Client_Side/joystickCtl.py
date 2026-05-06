import pyjoystick
import pickle
from pyjoystick.sdl2 import run_event_loop

class JoyController:

    def __init__(self):

        with open("settings.pkl", "rb") as f:
            self.data = pickle.load(f)

        self.status = "Disonnected"
        self.color = [0, 0, 255]
        self.yAxis = 0
        self.xAxis = 0
        self.steerVal = 7.5
        self.steerAngle = self.data["angle"]
        self.repeater = pyjoystick.HatRepeater(first_repeat_timeout=1, 
                                               repeat_timeout=0.1, 
                                               check_timeout=0.1)
        self.mngr = pyjoystick.ThreadEventManager(event_loop=run_event_loop,
                                                  add_joystick=self.add,
                                                  remove_joystick=self.remove,
                                                  handle_key_event=self.key_received,
                                                  button_repeater=self.repeater)

    def add(self, joy):
        self.status = "Connected"
        self.color = [0, 255, 0]
        #print(joyStatus)
    
    def remove(self, joy):
        self.status = "Disonnected"
        self.color = [0, 0, 255]
        #print(joyStatus)

    def key_received(self, key):
        #print(key, ": ", key.value)
        minAngle = 90 - self.steerAngle
        maxAngle = 90 + self.steerAngle
        minDC = (1/18) * minAngle + 2.5
        maxDC = (1/18) * maxAngle + 2.5
        if key == "Axis 1" or key == "-Axis 1":
            self.yAxis = int(key.value*100)
        if key == "Axis 3" or key == "-Axis 3":
            self.xAxis = int(key.value*100)
            self.steerVal = float(((maxDC - minDC) / 2) * (key.value + 1) + minDC)

    def listen(self):
        self.mngr.start()

    def setOptions(self, angle):
        self.steerAngle = angle