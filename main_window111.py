
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore

import cv2

from ui_main_window112 import *
import time

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ct = 1
        self.cameraTimer = QTimer()
        self.cameraTimer.timeout.connect(self.viewCam)
        self.ui.control_bt.clicked.connect(self.cameraTimerFunc)
        self.flag = 0
            
    # view camera
    def viewCam(self):
            
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        scale_percent = 50  # percent of original size
        new_w = int(image.shape[1] * scale_percent / 100)
        new_h = int(image.shape[0] * scale_percent / 100)
        dim = (new_w, new_h)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        step = channel * new_w
        qImg = QImage(resized.data, new_w, new_h, step, QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    def cameraTimerFunc(self):
        if not self.cameraTimer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.cameraTimer.start(10)
            self.ui.control_bt.setText("Stop")
        else:
            self.cameraTimer.stop()
            self.cap.release()
            self.ui.control_bt.setText("Start")

    #for chart
    def plotTimerFunc(self):
        if not self.plotTimer.isActive():
            self.ui.start_Time = time.time()
            self.plotTimer.start(0)
        else:
            self.plotTimer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
