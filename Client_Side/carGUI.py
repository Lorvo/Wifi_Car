from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pickle

class carGUI:

    def __init__(self):

        with open("settings.pkl", "rb") as f:
            self.data = pickle.load(f)
        self.bend = self.data["bend"]
        self.slope = self.data["slope"]
        self.offset = self.data["offset"]
        self.angle = self.data["angle"]
        self.address = None

        self.app = QApplication([])

        ################################
        ########## CONTAINERS ##########
        ################################

        self.widgetContainer = QWidget()
        self.optionsContainer = QWidget()
        self.alertContainer = QWidget()

        ################################
        ############ LAYOUTS ###########
        ################################

        self.mainLayout = QVBoxLayout(self.widgetContainer)
        self.optionsLayout = QVBoxLayout(self.optionsContainer)
        self.alertLayout = QVBoxLayout(self.alertContainer)

        self.bendSliderLayout = QHBoxLayout()
        self.slopeSliderLayout = QHBoxLayout()
        self.offsetSliderLayout = QHBoxLayout()
        self.angleSliderLayout = QHBoxLayout()

        self.optionButtonsLayout = QHBoxLayout()
        self.pButtonLayout = QHBoxLayout()

        ################################
        ############ WINDOWS ###########
        ################################

        self.connectWindow = QMainWindow()
        self.connectWindow.setWindowTitle("Connect to Server")
        self.connectWindow.setGeometry(960 - 250, 540 - 150, 500, 300)
        self.connectWindow.setCentralWidget(self.widgetContainer)

        self.optionsWindow = QMainWindow()
        self.optionsWindow.setWindowTitle("Options")
        self.optionsWindow.setGeometry(960 + 340, 60, 250, 100)
        self.optionsWindow.setCentralWidget(self.optionsContainer)

        self.popupWin = QMainWindow()
        self.popupWin.setWindowTitle("Alert")
        self.popupWin.setGeometry(960 - 125, 540 - 75, 250, 150)
        self.popupWin.setCentralWidget(self.alertContainer)
        
        ################################
        ############ BUTTONS ###########
        ################################

        self.saveOptionsButton = QPushButton('Save')
        self.saveOptionsButton.clicked.connect(self.save_options)

        self.revertOptionsButton = QPushButton('Revert')
        self.revertOptionsButton.clicked.connect(self.revert_options)

        self.localButton = QPushButton('Connect to Local')
        self.localButton.setStyleSheet("font-size: 24px; color: red; padding: 10px;")
        self.localButton.setFixedHeight(50)
        self.localButton.clicked.connect(self.local_connect)

        self.serverButton = QPushButton('Connect to server')
        self.serverButton.setStyleSheet("font-size: 24px; color: blue; padding: 10px;")
        self.serverButton.setFixedHeight(50)
        self.serverButton.clicked.connect(self.server_connect)

        self.okButton = QPushButton('OK')
        self.okButton.setStyleSheet("font-size: 24px; color: black; padding: 10px;")
        self.okButton.setFixedHeight(50)
        self.okButton.clicked.connect(self.on_ok)

        ################################
        ############ SLIDERS ###########
        ################################

        self.bendSlider = QSlider(Qt.Horizontal)
        self.bendSlider.setMinimum(0)
        self.bendSlider.setMaximum(4000)
        self.bendSlider.setValue(int(self.bend * 1000000))
        self.bendSlider.valueChanged.connect(self.bend_change)

        self.slopeSlider = QSlider(Qt.Horizontal)
        self.slopeSlider.setMinimum(0)
        self.slopeSlider.setMaximum(4000)
        self.slopeSlider.setValue(int(self.slope * 10000))
        self.slopeSlider.valueChanged.connect(self.slope_change)

        self.offsetSlider = QSlider(Qt.Horizontal)
        self.offsetSlider.setMinimum(0)
        self.offsetSlider.setMaximum(320)
        self.offsetSlider.setValue(self.offset)
        self.offsetSlider.valueChanged.connect(self.offset_change)

        self.angleSlider = QSlider(Qt.Horizontal)
        self.angleSlider.setMinimum(0)
        self.angleSlider.setMaximum(90)
        self.angleSlider.setValue(self.angle)
        self.angleSlider.valueChanged.connect(self.angle_change)

        ################################
        ############ LABELS ############
        ################################

        self.label = QLabel("Enter Server Link")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; color: black; padding: 10px;")
        self.label.setFixedHeight(50)
        self.warnLabel = QLabel("Invalid Server Address!!")
        self.warnLabel.setAlignment(Qt.AlignCenter)
        self.warnLabel.setStyleSheet("font-size: 24px; color: red; padding: 10px;")
        self.warnLabel.setFixedHeight(50)

        self.bendLabel = QLabel(f"Bend: {self.bendSlider.value() / 1000000}")
        self.slopeLabel = QLabel(f"Slope: {self.slopeSlider.value() / 10000}")
        self.offsetLabel = QLabel(f"Offset: {self.offsetSlider.value()}")
        self.angleLabel = QLabel(f"Angle: {self.angleSlider.value()}")

        ################################
        ############ TEXTBOX ###########
        ################################

        self.textbox = QLineEdit()
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setStyleSheet("font-size: 24px; color: black; padding: 10px;")
        self.textbox.setFixedHeight(50)

        ################################
        ######### ORGANISATION #########
        ################################        

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.textbox)
        self.mainLayout.addLayout(self.pButtonLayout)

        self.alertLayout.addWidget(self.warnLabel)
        self.alertLayout.addWidget(self.okButton)

        self.pButtonLayout.addWidget(self.localButton)
        self.pButtonLayout.addWidget(self.serverButton)

        self.bendSliderLayout.addWidget(self.bendLabel)
        self.bendSliderLayout.addWidget(self.bendSlider)

        self.slopeSliderLayout.addWidget(self.slopeLabel)
        self.slopeSliderLayout.addWidget(self.slopeSlider)

        self.offsetSliderLayout.addWidget(self.offsetLabel)
        self.offsetSliderLayout.addWidget(self.offsetSlider)

        self.angleSliderLayout.addWidget(self.angleLabel)
        self.angleSliderLayout.addWidget(self.angleSlider)

        self.optionsLayout.addLayout(self.bendSliderLayout)
        self.optionsLayout.addLayout(self.slopeSliderLayout)
        self.optionsLayout.addLayout(self.offsetSliderLayout)
        self.optionsLayout.addLayout(self.angleSliderLayout)
        self.optionsLayout.addLayout(self.optionButtonsLayout)

        self.optionButtonsLayout.addWidget(self.saveOptionsButton)
        self.optionButtonsLayout.addWidget(self.revertOptionsButton)

    ################################
    ########### CALLBACKS ##########
    ################################  

    def local_connect(self):
        self.address = ("192.168.1.241", 2222)
        self.connectWindow.close()

    def server_connect(self):
        textValue = self.textbox.text()
        try:
            textValue = textValue.replace("tcp://", "")
            self.address = (textValue.split(":")[0], int(textValue.split(":")[1]))
            self.connectWindow.close()
            self.popupWin.close()
        except:
            self.popupWin.show()
    
    def on_ok(self):
        self.popupWin.close()

    def bend_change(self):
        self.bend = self.bendSlider.value() / 1000000
        self.bendLabel.setText(f"Bend: {self.bendSlider.value() / 1000000}")

    def slope_change(self):
        self.slope = self.slopeSlider.value() / 10000
        self.slopeLabel.setText(f"Slope: {self.slopeSlider.value() / 10000}")

    def offset_change(self):
        self.offset = self.offsetSlider.value()
        self.offsetLabel.setText(f"Offset: {self.offsetSlider.value()}")

    def angle_change(self):
        self.angle = self.angleSlider.value()
        self.angleLabel.setText(f"Angle: {self.angleSlider.value()}")

    def save_options(self):
        data =  {
                "angle": self.angle,
                "bend": self.bend,
                "offset": self.offset,
                "slope": self.slope,
                }

        with open("settings.pkl", "wb") as f:
            pickle.dump(data, f)

    def revert_options(self):
        with open("settings.pkl", "rb") as f:
            self.data = pickle.load(f)
        self.bend = self.data["bend"]
        self.slope = self.data["slope"]
        self.offset = self.data["offset"]
        self.angle = self.data["angle"]
        self.bendSlider.setValue(int(self.bend * 1000000))
        self.slopeSlider.setValue(int(self.slope * 10000))
        self.offsetSlider.setValue(self.offset)
        self.angleSlider.setValue(self.angle)

    ################################
    ############ METHODS ###########
    ################################  

    def runConnectGUI(self):
        self.connectWindow.show()
        self.app.exec_()

    def runSettingsGUI(self):
        self.optionsWindow.show()
