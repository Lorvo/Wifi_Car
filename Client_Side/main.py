from communication import CarConn
from imgProcessing import Feed
from joystickCtl import JoyController
from carGUI import carGUI

myGUI = carGUI()
myGUI.runConnectGUI()

myCar = CarConn(myGUI.address[0], myGUI.address[1], 30000)
myGUI.runSettingsGUI()
myFeed = Feed(640, 480)
myController = JoyController()

myController.listen()

while True:
    myCar.sendData(str(myController.steerVal) + "," + str(myController.yAxis))
    myFeed.setOptions(myGUI.bend, myGUI.slope, myGUI.offset, myGUI.angle)
    myController.setOptions(myGUI.angle)
    myFeed.calculateBend(myController.xAxis)
    myFeed.showEncodedImg(myCar.recvData(), myController.status, myController.color)