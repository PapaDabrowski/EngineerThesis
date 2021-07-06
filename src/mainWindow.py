import sys
import numpy as np

#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#Internal imports
import constants

from chooseType import ui_ChooseType
from chooseDevice import ui_ChooseDevice
from signalGenerator import ui_SignalGenerator
from errorBox import ui_ErrorBox
from osciloscope import ui_Osciloscope
from multimeter import ui_Multimeter

from pV import pyVisaInterface

class ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main Window UI class

    That class provides UI which helps with managing whole app.
    That class basicly contains handlers for all nested windows. 
    Also that class provides components requires for nested windows.

    Attributes
    ----------

    Methods
    -------
    cancelMethod(self):
        close window function

    deleteElement(self, string):
        method for all nested windows to inform main window about closing event
    """

    def __init__(self, pyVisaInit):
        super(ui_MainWindow, self).__init__()

        uic.loadUi("../UI/mainPanel.ui", self)
        self.__controlers=[]
        self.__window=[]

        self.__newControlerButton = self.findChild(QtWidgets.QPushButton, 'addControler')
        self.__newControlerButton.clicked.connect(self.__addNextControler)

        self.__infoLog = self.findChild(QtWidgets.QListWidget, 'listWidget')

        #self.__pyVisa = pyVisaInterface('C:\Windows\System32\\visa64.dll',self.__infoLog) #temporary specifier "@sim" it's basicly a mock
        self.__pyVisa = pyVisaInterface(pyVisaInit, self.__infoLog) #temporary specifier "@sim" it's basicly a mock

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, (QMessageBox.No))
        if reply == QMessageBox.Yes:
            if not self.__controlers and not self.__window:
                event.accept()
            else:
                QMessageBox.information(self, 'Warning', 'Cannot close main window when other instances are opened!')
                event.ignore()
        else:
            event.ignore()

    def callBackDeviceType(self, string):
        if string == constants.MULTIMETER:
            self.__controlers.append(ui_Multimeter(self, self.__pyVisa))
        elif string == constants.OSCILLOSCOPE:
            #self.controlers.append(ui_Osciloscope(self))
            self.__errorWindow = ui_ErrorBox(9999999999)
        elif string == constants.SIGNALGENERATOR:
            self.__controlers.append(ui_SignalGenerator(self, self.__pyVisa))

    def deleteElement(self, string):
        if string == constants.EXTERNALWINDOW:
            self.__controlers.pop()
        elif string == constants.INTERNALWINDOW:
            self.__window.pop()

    def __addNextControler(self):
        self.__deviceTypeTemp = ""
        if not self.__window:
            self.__window.append(ui_ChooseType(self, self.callBackDeviceType))