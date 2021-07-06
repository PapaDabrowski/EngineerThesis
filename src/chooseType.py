import sys
import numpy as np

#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#Internal imports
import constants

class ui_ChooseType(QtWidgets.QWidget):
    def __init__(self, external,callBack):
        super(ui_ChooseType, self).__init__()
        self.__callBack = callBack
        self.__external = external

        uic.loadUi("../UI/chooseType.ui", self)

        self.__multimeterButton = self.findChild(QtWidgets.QPushButton, 'multimeterButton')
        self.__multimeterButton.clicked.connect(self.__multimeter)

        self.__oscilloscopeButton = self.findChild(QtWidgets.QPushButton, 'osciloscopeButton')
        self.__oscilloscopeButton.clicked.connect(self.__oscilloscope)

        self.__signalGeneratorButton = self.findChild(QtWidgets.QPushButton, 'signalGeneratorButton')
        self.__signalGeneratorButton.clicked.connect(self.__signalGenerator)

        self.show()

    def closeEvent(self, event):
        self.__external.deleteElement(constants.INTERNALWINDOW)
        event.accept()

    def __multimeter(self):
        self.__callBackFun(constants.MULTIMETER)

    def __oscilloscope(self):
        self.__callBackFun(constants.OSCILLOSCOPE)

    def __signalGenerator(self):
        self.__callBackFun(constants.SIGNALGENERATOR)

    def __callBackFun(self, string):
        self.__callBack(string)
        self.close()