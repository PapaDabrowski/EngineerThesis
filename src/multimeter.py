import sys
import numpy as np
import time

#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator

#Internal imports
import constants

from chooseDevice import ui_ChooseDevice
from errorBox import ui_ErrorBox

from pV import pyVisaInterface

class ui_Multimeter(QtWidgets.QMainWindow):
    """
    Template signal generator manager class

    That class provides UI which allows user to easy manage signal generator.
    Outside caller have to provide to initialize that object, pyVisaInterface which
    is required for low-level communication with device. Also caller have to provide hook to himself,
    and caller have to implement function "void deleteElement(self)", all details are explaind below.
    Class base on self-sufficient approach, and thanks to that it's quiet easy to use and connect 
    that UI interface to any kind of programs. Class do not share any public functions.

    Attributes
    ----------
    external : parent object
        It allows to inform parent object about state
    pyVisa : pyVisaInterface
        VISA interface wrapper
    textBrowser : QtWidgets.QTextBrowser
        UI widget text browser responsible for showing address of selected device
    confirmButton : QtWidgets.QPushButton
        UI widget button which opens widget to choose device
    nameOfDeviceTextBrowser : QtWidgets.QTextBrowser
        UI widget text browser responsible for showing name of selected device
    valueDisplay : QtWidgets.QLCDNumber
        UI widget LCD Display which shows current value
    rangeInfoTextBrowser : QtWidgets.QTextBrowser
        UI widget text browser responsible for showing metric prefix
    modeSelector : QtWidgets.QComboBox
        UI widget combo box which allow to select the shape of output function
    metricPrefixSelector : QtWidgets.QComboBox
        UI widget combo box which allot to select metric prefix
    measureButton : QtWidgets.QPushButton
        UI widget button which call measure start method
    autoMeasureButton : QtWidgets.QPushButton
        UI widget button which call automeasure start method
    statusTextBrowser : QtWidgets.QTextBrowser
        UI widget text browser which shows status of connection
    checkErrorButton : QtWidgets.QPushButton
        UI widget button which calls all parameters checking function
    window : ui_ChooseDevice
        UI widget for choosing device hook
    baudRate : int
        Baud Rate value for specifed device
    errorWindow : ui_ErrorBox
        UI widget for error window hook

    Methods
    -------
    closeEvent(self, event):
        function which overrides closeEvent fun

    """

    def __init__(self, external, pyVisa):
        super(ui_Multimeter, self).__init__()
        self.__external = external
        self.__pyVisa = pyVisa
        uic.loadUi("../UI/multimeter.ui", self)

        self.textBrowser = self.findChild(QtWidgets.QTextBrowser,'textBrowser')
        self.textBrowser.setReadOnly(True)

        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton')
        self.confirmButton.clicked.connect(self.__chooseDeviceWindow)

        self.nameOfDeviceTextBrowser = self.findChild(QtWidgets.QTextBrowser,'nameOfDeviceTextBrowser')
        self.nameOfDeviceTextBrowser.setReadOnly(True)

        self.valueDisplay = self.findChild(QtWidgets.QLCDNumber, 'valueDisplay')
        self.valueDisplay.setStyleSheet("background-color: rgb(0, 0, 0);border: 2px solid rgb(113, 113, 113);border-width: 2px;border-radius: 10px;color: rgb(239, 245, 66);")
        self.valueDisplay.setDigitCount(12)
        self.valueDisplay.setSmallDecimalPoint(True)

        self.rangeInfoTextBrowser = self.findChild(QtWidgets.QTextBrowser,'rangeInfoTextBrowser')
        self.rangeInfoTextBrowser.setStyleSheet("background-color: rgb(0, 0, 0);border: 2px solid rgb(113, 113, 113);border-width: 2px;border-radius: 10px;color: rgb(239, 245, 66);")
        self.rangeInfoTextBrowser.setReadOnly(True)
        self.rangeInfoTextBrowser.append('-')

        self.modeSelector = self.findChild(QtWidgets.QComboBox, 'modeSelector')
        self.modeSelector.addItem(constants.VOLTAGE_AC)
        self.modeSelector.addItem(constants.VOLTAGE_DC)
        self.modeSelector.addItem(constants.CURRENT_DC)
        self.modeSelector.addItem(constants.CURRENT_AC)
        self.modeSelector.addItem(constants.RESISTANCE)
        self.modeSelector.addItem(constants.FRESISTANCE)
        self.modeSelector.addItem(constants.FREQUENCY)
        self.modeSelector.addItem(constants.PERIOD)

        self.metricPrefixSelector = self.findChild(QtWidgets.QComboBox, 'metricPrefixSelector')
        self.metricPrefixSelector.addItem(constants.signMicro)
        self.metricPrefixSelector.addItem(constants.signMili)
        self.metricPrefixSelector.addItem(constants.signNone)
        self.metricPrefixSelector.addItem(constants.signKilo)
        self.metricPrefixSelector.addItem(constants.signMega)
        self.metricPrefixSelector.setCurrentIndex(2)

        self.measureButton = self.findChild(QtWidgets.QPushButton, 'measureButton')
        self.measureButton.clicked.connect(self.__measureStart)

        self.autoMeasureButton = self.findChild(QtWidgets.QPushButton, 'autoMeasureButton')
        self.autoMeasureButton.clicked.connect(self.__auto)

        self.statusTextBrowser = self.findChild(QtWidgets.QTextBrowser,'statusTextBrowser')
        self.statusTextBrowser.setReadOnly(True)
        self.statusTextBrowser.append(self.__pyVisa.getDeviceStatus())

        self.checkErrorButton = self.findChild(QtWidgets.QPushButton, 'checkErrorButton')   
        self.checkErrorButton.clicked.connect(self.__pyVisa.checkErrorBus)

        self.show()

    def closeEvent(self, event):
        """Close Event Function

        That functions is invoked when user try to close window.
        Function creates MassageBox to ask user sure to close the window.

        Parameters
        ----------
        event :
            event occured on window
        """

        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, (QMessageBox.No))
        if reply == QMessageBox.Yes:
            self.__external.deleteElement(constants.EXTERNALWINDOW)
            event.accept()
        else:
            event.ignore()

    def __callBackAppendDeviceName(self, string):
        """CallBack for getting device name

        That function provide name of device after gets
        invoked and insert that name into textBrowser

        Parameters
        ----------
        string : str
            recived name of device
        """

        self.nameOfDeviceTextBrowser.clear()
        self.nameOfDeviceTextBrowser.append(string)

    def __callBackChooseDevice(self, string, baudRate):
        """CallBack for choosing device

        That function provide address of device and
        baud rate after gets invoked. Callback also
        insert address in textBrowser
        At the end it calls __configureInstrument()[more details below]

        Parameters
        ----------
        string : str
            address of device
        baudRate : int
            baud rate provided by user
        """

        self.textBrowser.clear()
        self.textBrowser.append(string)

        self.nameOfDeviceTextBrowser.clear()
        self.statusTextBrowser.clear()

        self.baudRate = baudRate

        self.__configureInstrument()
        if self.__pyVisa.getDeviceStatus() == constants.CONFIGURED:
            self.__pyVisa.getDeviceName(self.__callBackAppendDeviceName)

    def __chooseDeviceWindow(self):
        """Choose device Window

        It's hook for choosing device, from all avalivable connected devices.
        Here we also provide callback which will be invoked after user
        choose device.
        """

        self.window = ui_ChooseDevice(self.__pyVisa, self.__callBackChooseDevice)

    def __configureInstrument(self):
        instrumentName = self.textBrowser.toPlainText()
        if instrumentName:
            self.__pyVisa.openResource(instrumentName)
            if self.__pyVisa.getDeviceStatus() == constants.OPENED:
                self.__pyVisa.configureCommunication(self.baudRate)
                self.statusTextBrowser.append(self.__pyVisa.getDeviceStatus())
            else:
                self.errorWindow = ui_ErrorBox(1000000101)

    def __auto(self):
        if self.__pyVisa.getDeviceStatus() == constants.CONFIGURED:
            self.__setInfo(self.__convertModeToUnit(str(self.modeSelector.currentText())), constants.signNone)
            self.__pyVisa.autoMeasure(str(self.modeSelector.currentText()), __callBackOnMeasureDone)
        else:
            self.errorWindow = ui_ErrorBox(1000000100)

    def __measureStart(self):
        if self.__pyVisa.getDeviceStatus() == constants.CONFIGURED:
            self.__setInfo(self.__convertModeToUnit(str(self.modeSelector.currentText())),str(self.metricPrefixSelector.currentText()))
        else:
            self.errorWindow = ui_ErrorBox(1000000100)

    def __setInfo(self, stringMode, stringMetricPrefix):
        self.rangeInfoTextBrowser.clear()
        self.rangeInfoTextBrowser.append(stringMetricPrefix + stringMode)

    def __convertModeToUnit(self, string):
        if string == constants.VOLTAGE_AC or string == constants.VOLTAGE_DC:
            return constants.unitVoltage
        elif string == constants.CURRENT_AC or string == constants.CURRENT_DC:
            return constants.unitCurrent
        elif string == constants.RESISTANCE or string == constants.FRESISTANCE:
            return constants.unitResistance
        elif string == constants.FREQUENCY:
            return constants.unitFrequency
        elif string == constants.PERIOD:
            return constants.unitPeroid
        else:
            return constatns.ERROR

    def __callBackOnMeasureDone(string):
        self.__convertToDisplay(string)

    def __convertToDisplay(string):
        pass
        #zmiana na normalne wartości
