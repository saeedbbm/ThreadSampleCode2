
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
import numpy as np
import time
import qwt
import pyqtgraph as pg
from threading import Thread
from collections import deque


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):

        return [QtCore.QTime().currentTime().addMSecs(value).toString('mm:ss') for value in values]

class LocationAxisItem(pg.AxisItem):
    def __init__(self,x, *args, **kwargs):
        super(LocationAxisItem, self).__init__(*args, **kwargs)
        self.myXtick = x

    def tickStrings(self, values, scale, spacing):

        print(self.myXtick)
        return [self.myXtick]

class ScrollingTimestampPlot(QtGui.QWidget):

    def __init__(self,DATA_POINTS_TO_DISPLAY, parent=None):
        super(ScrollingTimestampPlot, self).__init__(parent)

        self.timestamp = QtCore.QTime()
        self.timestamp.start()

        self.DATA_POINTS_TO_DISPLAY = DATA_POINTS_TO_DISPLAY

        self.data1 = deque(maxlen=self.DATA_POINTS_TO_DISPLAY)

        # Create Plot Widget
        self.scrolling_timestamp_plot_widget = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})#,'top': LocationAxisItem(self.x,orientation='top')})
        self.scrolling_timestamp_plot_widget.showGrid(x=True, y=True, alpha=0.2)

        self.scrolling_timestamp_plot_widget.plotItem.setMouseEnabled(x=False, y=False)

        self.scrolling_timestamp_plot_widget.setTitle('Sound vs Time')
        self.scrolling_timestamp_plot_widget.setLabel('left', 'Value')
        self.scrolling_timestamp_plot_widget.setLabel('bottom', 'Time (s)')

        self.scrolling_timestamp_plot = self.scrolling_timestamp_plot_widget.plot()

        self.scrolling_timestamp_plot.setPen(pg.mkPen('b', width=5, style=QtCore.Qt.DotLine))

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.scrolling_timestamp_plot_widget)

        self.read_position_thread()
        self.start()

    def start(self):

        self.position_update_timer = QtCore.QTimer()
        self.position_update_timer.timeout.connect(self.plot_updater)
        self.position_update_timer.start(self.get_scrolling_timestamp_plot_refresh_rate())

    def read_position_thread(self):
        self.current_position_value = 0
        self.position_update_thread = Thread(target=self.read_position, args=())
        self.position_update_thread.daemon = True
        self.position_update_thread.start()

    def read_position(self):
        frequency = 0.1#self.get_scrolling_timestamp_plot_frequency()
        while True:
            self.current_position_value = random.randint(1,101)
            time.sleep(frequency)

    def plot_updater(self):
        self.data_point = float(self.current_position_value)
        self.data1.append({'x': self.timestamp.elapsed(), 'y': self.data_point})
        self.x = [item['x'] for item in self.data1]
        self.y = [item['y'] for item in self.data1]
        self.scrolling_timestamp_plot.setData(self.x,self.y)

    def clear_scrolling_timestamp_plot(self):
        self.data1.clear()

    def get_scrolling_timestamp_plot_frequency(self):
        return self.FREQUENCY

    def get_scrolling_timestamp_plot_refresh_rate(self):
        return 0.1#self.SCROLLING_TIMESTAMP_PLOT_REFRESH_RATE

    def get_scrolling_timestamp_plot_layout(self):
        return self.layout

    def get_current_position_value(self):
        return self.current_position_value

    def get_scrolling_timestamp_plot_widget(self):
        return self.scrolling_timestamp_plot_widget

class Ui_Form(object):
    def __init__(self):
        
        self.start_Time = 0
        self.t0 = 0
        self.X0 = 0
        self.V0 = 0
        self.V1 = 0
        self.y_val = 0
        self.t_val = 0

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1020, 700)

        self.x_val = 0
        
        self.wlayout = QtWidgets.QVBoxLayout(Form)
        #horizental with camra & chart
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.image_label)
        
        self.control_bt = QtWidgets.QPushButton()
        self.verticalLayout.addWidget(self.control_bt)
        
        self.horizontalLayout.addLayout(self.verticalLayout, 2)
        
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.verticalLayout2.setContentsMargins(0,0,0,0)
        self.verticalLayout2.setSpacing(0)
        self.label2 = QtWidgets.QLabel("chart")

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        DATA_POINTS_TO_DISPLAY_1 = 20
        self.scrolling_timestamp_plot_widget1 = ScrollingTimestampPlot(DATA_POINTS_TO_DISPLAY_1)
        self.verticalLayout2.addWidget(self.scrolling_timestamp_plot_widget1.get_scrolling_timestamp_plot_widget())

        self.horizontalLayout.addLayout(self.verticalLayout2, 1)
        self.wlayout.addLayout(self.horizontalLayout, 3)
        #chart2
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")

        self.verticalLayout3 = QtWidgets.QVBoxLayout()
        self.verticalLayout3.setObjectName("verticalLayout3")
        self.verticalLayout3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout3.setSpacing(0)

        self.label4 = QtWidgets.QLabel(str (self.x_val))
        font = self.label4.font()
        font.setPointSize(30)
        font.setBold(True)
        self.label4.setFont(font)
        self.verticalLayout3.addWidget(self.label4 )

        self.label5 = QtWidgets.QLabel("  location")
        font2 = self.label5.font()
        font2.setPointSize(13)
        font2.setBold(True)
        self.label5.setFont(font2)
        self.verticalLayout3.addWidget(self.label5)

        self.verticalLayout4 = QtWidgets.QVBoxLayout()
        self.verticalLayout4.setObjectName("verticalLayout4")
        self.verticalLayout4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout4.setSpacing(0)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        DATA_POINTS_TO_DISPLAY_2 = 200
        self.scrolling_timestamp_plot_widget2 = ScrollingTimestampPlot(DATA_POINTS_TO_DISPLAY_2)
        self.verticalLayout4.addWidget(self.scrolling_timestamp_plot_widget2.get_scrolling_timestamp_plot_widget())

        self.horizontalLayout2.addLayout(self.verticalLayout3, 1)
        self.horizontalLayout2.addLayout(self.verticalLayout4, 9)
        self.wlayout.addLayout(self.horizontalLayout2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Leak Detection"))
        self.control_bt.setText(_translate("Form", "Start"))
