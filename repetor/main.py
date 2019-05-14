import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
import serial.tools.list_ports
import time
import os


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'WiFi Extender'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.portList = []
        self.wifiList = []

        #window icon
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'pp.png'))

        #init window
        self.initUI()

    #get all available ports
    def getPorts(self):
        comPorts = list(serial.tools.list_ports.comports())

        for i in range(0,len(comPorts)):
            l = str(comPorts[i])
            l = l.split("-")
            a = l[0]
            a = a[:-1]
            self.portList.append(a)

    def initUI(self):
        self.getPorts()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)



        #PORT
        self.labelID = QtWidgets.QLabel(self)
        self.labelID.setText("PORT:  ")
        self.labelID.move(40, 17)

        self.comboPorts = QComboBox(self)
        for i in self.portList:
            self.comboPorts.addItem(i)

        self.comboPorts.move(40, 40)
        self.comboPorts.resize(120, 23)

        #AUTOMESH ON/OFF
        self.labelMesh = QtWidgets.QLabel(self)
        self.labelMesh.setText("Automesh:")
        self.labelMesh.move(70, 90)

        self.buttonMeshOn = QPushButton('ON', self)
        self.buttonMeshOn.move(40, 120)
        self.buttonMeshOn.resize(50, 30)

        self.buttonMeshOff = QPushButton('OFF', self)
        self.buttonMeshOff.move(100, 120)
        self.buttonMeshOff.resize(50, 30)


        #WIFI SETTINGS
        self.labelID = QtWidgets.QLabel(self)
        self.labelID.setText("WiFi ID: ")
        self.labelID.move(250, 17)

        self.textbox1_1 = QLineEdit(self)
        self.textbox1_1.move(250, 40)
        self.textbox1_1.resize(120, 23)

        self.labelPass = QtWidgets.QLabel(self)
        self.labelPass.setText("WiFi Password: ")
        self.labelPass.move(250, 60)

        self.textbox1_2 = QLineEdit(self)
        self.textbox1_2.move(250, 85)
        self.textbox1_2.resize(120, 23)

        self.button1 = QPushButton('Set', self)
        self.button1.move(250, 120)
        self.button1.resize(50, 30)


        #AP CHANGE
        self.labelApID = QtWidgets.QLabel(self)
        self.labelApID.setText("AP ID: ")
        self.labelApID.move(450,17)

        self.textbox2_1 = QLineEdit(self)
        self.textbox2_1.move(450, 40)
        self.textbox2_1.resize(120, 23)

        self.labelApPass = QtWidgets.QLabel(self)
        self.labelApPass.setText("AP Pass: ")
        self.labelApPass.move(450, 60)

        self.textbox2_2 = QLineEdit(self)
        self.textbox2_2.move(450,85)
        self.textbox2_2.resize(120, 23)

        self.button2 = QPushButton('Change', self)
        self.button2.move(450, 120)
        self.button2.resize(50,30)

        #SCAN
        self.labelScan = QtWidgets.QLabel(self)
        self.labelScan.setText("Scan for WiFi:")
        self.labelScan.move(40, 234)

        self.comboWifi = QComboBox(self)
        self.comboWifi.move(40, 300)
        self.comboWifi.resize(150, 23)

        self.buttonScan = QPushButton('Scan', self)
        self.buttonScan.move(40, 260)
        self.buttonScan.resize(50, 30)

        self.buttonScanOk = QPushButton('OK', self)
        self.buttonScanOk.move(200, 300)
        self.buttonScanOk.resize(50, 25)

        #RESET
        self.labelReset = QtWidgets.QLabel(self)
        self.labelReset.setText("Factory Reset: ")
        self.labelReset.move(400, 234)

        self.buttonReset = QPushButton('RESET', self)
        self.buttonReset.move(400, 260)
        self.buttonReset.resize(50, 30)

        #BOARD INFO
        self.labelShow = QtWidgets.QLabel(self)
        self.labelShow.setText("Board Info: ")
        self.labelShow.move(500, 234)

        self.buttonShow = QPushButton('SHOW', self)
        self.buttonShow.move(500, 260)
        self.buttonShow.resize(50, 30)



        self.button1.clicked.connect(self.b1_click)
        self.show()

        self.button2.clicked.connect(self.b2_click)
        self.show()

        self.buttonMeshOn.clicked.connect(self.mesh_on_click)
        self.show()

        self.buttonMeshOff.clicked.connect(self.mesh_off_click)
        self.show()

        self.buttonScan.clicked.connect(self.scan_click)
        self.show()

        self.buttonScanOk.clicked.connect(self.scanOk_click)
        self.buttonScanOk.setEnabled(False)
        self.show()

        self.buttonReset.clicked.connect(self.reset_click)
        self.show()

        self.buttonShow.clicked.connect(self.show_click)
        self.show()

    #SET button
    def b1_click(self):
        if not self.textbox1_1.text():
            QMessageBox.about(self, "ERROR", "The SSID cannot be empty!")
            return 0
        if not self.textbox1_2.text():
            QMessageBox.about(self, "ERROR", "The PASSWORD cannot be empty!")
            return 0

        id = self.textbox1_1.text()
        passw = self.textbox1_2.text()

        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .1

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR","Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            try:
                ser.write(("set ssid " + id).encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("set password " + passw).encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("save").encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("reset").encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
            except:
                QMessageBox.about(self, "ERROR", "Make sure you have entered a valid SSID and PASSWORD!")
            else:
                ser.close()


    #CHANGE button
    def b2_click(self):
        if not self.textbox2_1.text():
            QMessageBox.about(self, "ERROR", "The SSID cannot be empty!")
            return 0
        if not self.textbox2_2.text():
            QMessageBox.about(self, "ERROR", "The PASSWORD cannot be empty!")
            return 0

        ApID = self.textbox2_1.text()
        APPass = self.textbox2_2.text()

        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .1

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR","Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            try:
                ser.write(("set ap_ssid "+ApID).encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("set ap_password " + APPass).encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("save").encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
                ser.write(("reset").encode() + b'\x0d' + b'\x0a')
                time.sleep(2)
            except:
                QMessageBox.about(self, "ERROR", "Make sure you have entered a valid SSID and PASSWORD!")
            else:
                ser.close()


    def mesh_on_click(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .1

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR","Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            ser.write(("set automesh 1").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)
            ser.write(("save").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)
            ser.write(("reset").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)

            ser.close()

    def mesh_off_click(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .1

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR", "Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            ser.write(("set automesh 0").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)
            ser.write(("save").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)
            ser.write(("reset").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)

            ser.close()

    #scan for wifis and print to window
    def scan_click(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = 10
        self.comboWifi.clear()

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR", "Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)
            print("hey")
            ser.write(("scan").encode() + b'\x0d' + b'\x0a')
            time.sleep(5)
            text = ser.read_all()
            text = text.decode('utf-8','ignore')
            print("hey")
            sep = 'scandone'
            wifi = text.split(sep)[2]
            wifi=wifi[:-4]
            print("hey")
            wifi = wifi.split(",")
            i=1

            print(wifi)

            while i<len(wifi):
                if(wifi[i].find('mask')!=-1):
                    break

                self.comboWifi.addItem(wifi[i])
                i = i+4

            self.buttonScanOk.setEnabled(True)

            ser.close()

    def scanOk_click(self):
        text = self.comboWifi.currentText()

        l = text.split('"')
        text = l[1]

        self.textbox1_1.setText(text)

    def reset_click(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .1

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR", "Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            ser.write(("reset factory").encode() + b'\x0d' + b'\x0a')
            time.sleep(2)

            ser.close()

    def show_click(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = self.comboPorts.currentText()
        ser.timeout = .5

        try:
            ser.open()
        except:
            QMessageBox.about(self, "ERROR", "Make sure you have entered a valid PORT!")
        else:
            time.sleep(5)

            ser.write(("show").encode() + b'\x0d' + b'\x0a')
            time.sleep(5)
            text = ser.read_all()
            text = text.decode('utf-8','ignore')

            sep = 'show'
            text = text.split(sep)[1]
            text = text.split('CMD')[0]

            QMessageBox.about(self, "Board Info", text)

            print(text)









if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())

