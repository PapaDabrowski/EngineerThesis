import sys
import numpy as np

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

class ui_SignalGenerator(QtWidgets.QMainWindow):
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
    waveFormSelector : QtWidgets.QComboBox
        UI widget combo box which allow to select the shape of output function
    frequencyLineEdit : QtWidgets.QLineEdit
        UI widget line edit to enter the frequency value
    amplitudeLineEdit : QtWidgets.QLineEdit
        UI widget line edit to enter the amplitude value
    offSetCheckBox : QtWidgets.QCheckBox
        UI widget check box which enable offset-line-edit to enter the value
    offsetLineEdit : QtWidgets.QLineEdit
        UI widget line edit to enter the amplitude value
    applyButton : QtWidgets.QPushButton
        UI widget button that sends all data to device and apply generation process
    modulationCheckBox : QtWidgets.QCheckBox
        UI widget check box which enable modulation and allows to enter the values
    modulationSelector : QtWidgets.QComboBox
        UI widget combo box which allow to select the modulating waveform
    frequencyModulationLineEdit : QtWidgets.QLineEdit
        UI widget line edit to enter the frequency modulation value
    depthDeviationLineEdit : QtWidgets.QLineEdit
        UI widget line edit to enter the depth/deviation modulation value
    modulatingWaveformSelector : QtWidgets.QComboBox
        UI widget combo box which allow to select the modulation carrier waveform
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
        """Initialization Method

        In init all UI widgets get assigned to hook variables.

        Parameters
        ----------
        external : parent object
            It allows to inform parent object about state
        pyVisa : pyVisaInterface
            VISA interface wrapper
        """

        super(ui_SignalGenerator, self).__init__()
        self.__external = external
        self.__pyVisa = pyVisa
        uic.loadUi("../UI/signalGenerator.ui", self)

        self.__textBrowser = self.findChild(QtWidgets.QTextBrowser,'textBrowser')
        self.__textBrowser.setReadOnly(True)

        self.__confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton')
        self.__confirmButton.clicked.connect(self.__chooseDeviceWindow)

        self.__nameOfDeviceTextBrowser = self.findChild(QtWidgets.QTextBrowser,'nameOfDeviceTextBrowser')
        self.__nameOfDeviceTextBrowser.setReadOnly(True)


        self.__waveFormSelector = self.findChild(QtWidgets.QComboBox, 'waveFormSelector')
        self.__waveFormSelector.addItem(constants.SINUS)
        self.__waveFormSelector.addItem(constants.SQUARE)
        self.__waveFormSelector.addItem(constants.TRIANGLE)
        self.__waveFormSelector.addItem(constants.RAMP)
        self.__waveFormSelector.addItem(constants.NOISE)
        self.__waveFormSelector.addItem(constants.DC)
        self.__waveFormSelector.activated[str].connect(self.__onWaveFormChanged)

        #For Agilent 33120A
        #Values for this device from 100 uHz up to 15 MHz
        #Sine           100 uHz to 15  MHz
        #Square         100 uHz to 15  MHz
        #Ramp           100 uHz to 100 kHz
        #Triangle       100 uHz to 100 kHz
        #Built-In Arbs  100 uHz to 5   MHz
        #*For Specifed waveforms this values can be diffrent
        self.__frequencyLineEdit = self.findChild(QtWidgets.QLineEdit, 'frequencyLineEdit')
        regex = QRegExp("(([0-9]{1,8})((\.([0-9]{1,8})))?)")
        inputValidator = QRegExpValidator(regex, self.__frequencyLineEdit)
        self.__frequencyLineEdit.setValidator(inputValidator)

        #For Agilent 33120A
        #Values for this device for 50 Ohm
        #Sine           50 mVpp to  10 Vpp
        #Square         50 mVpp to  10 Vpp
        #Ramp           50 mVpp to  10 Vpp
        #Triangle       50 mVpp to  10 Vpp
        #Noise          50 mVpp to  10 Vpp
        #Built-In Arbs  50 mVpp to  10 Vpp
        #*For Specifed waveforms this values can be diffrent
        self.__amplitudeLineEdit = self.findChild(QtWidgets.QLineEdit, 'amplitudeLineEdit')
        regexAmp = QRegExp("(([0-9]{1,8})((\.([0-9]{1,8})))?)")
        inputValidatorAmp = QRegExpValidator(regexAmp, self.__amplitudeLineEdit)
        self.__amplitudeLineEdit.setValidator(inputValidatorAmp)

        self.__offSetCheckBox = self.findChild(QtWidgets.QCheckBox, 'offSetCheckBox')
        self.__offSetCheckBox.toggled.connect(self.__onCheckedOffSet)

        self.__offsetLineEdit = self.findChild(QtWidgets.QLineEdit, 'offsetLineEdit')
        regexoffSet = QRegExp("[-]?(([0-9]{1,2})((\.([0-9]{1,8})))?)")
        inputValidatorOffSet = QRegExpValidator(regexoffSet, self.__offsetLineEdit)
        self.__offsetLineEdit.setValidator(inputValidatorOffSet)
        self.__offsetLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
        self.__offsetLineEdit.setReadOnly(True)

        self.__applyButton = self.findChild(QtWidgets.QPushButton, 'applyButton')
        self.__applyButton.clicked.connect(self.__insertToGenerator)

        self.__modulationCheckBox = self.findChild(QtWidgets.QCheckBox, 'modulationCheckBox')
        self.__modulationCheckBox.toggled.connect(self.__onCheckedModulation)

        self.__modulationSelector = self.findChild(QtWidgets.QComboBox, 'modulationSelector')
        self.__modulationSelector.addItem(constants.FM)
        self.__modulationSelector.addItem(constants.AM)
        self.__modulationSelector.activated[str].connect(self.__onModulationChanged)

        #For Agilent 33120A
        #AM           10 mHz to 20 kHz
        #FM           10 mHz to 10 kHz
        self.__frequencyModulationLineEdit = self.findChild(QtWidgets.QLineEdit, 'frequencyModulationLineEdit')
        regex = QRegExp("(([0-9]{1,5})((\.([0-9]{1,3})))?)")
        inputValidatorfrequencyModulation = QRegExpValidator(regex, self.__frequencyModulationLineEdit)
        self.__frequencyModulationLineEdit.setValidator(inputValidatorfrequencyModulation)
        self.__frequencyModulationLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
        self.__frequencyModulationLineEdit.setReadOnly(True)

        #For Agilent 33120A
        #AM Depth     0  %   to 120 %
        #FM Deviation 10 mHz to 7.5 MHz
        self.__depthDeviationLineEdit = self.findChild(QtWidgets.QLineEdit, 'depthDeviationLineEdit')
        regex = QRegExp("(([0-9]{1,8})((\.([0-9]{1,3})))?)")
        inputValidatordepthDeviationLineEdit = QRegExpValidator(regex, self.__depthDeviationLineEdit)
        self.__depthDeviationLineEdit.setValidator(inputValidatordepthDeviationLineEdit)
        self.__depthDeviationLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
        self.__depthDeviationLineEdit.setReadOnly(True)

        self.__modulatingWaveformSelector = self.findChild(QtWidgets.QComboBox, 'modulatingWaveformSelector')
        self.__modulatingWaveformSelector.addItem(constants.SINUS)
        self.__modulatingWaveformSelector.addItem(constants.SQUARE)
        self.__modulatingWaveformSelector.addItem(constants.TRIANGLE)
        self.__modulatingWaveformSelector.addItem(constants.RAMP)
        self.__modulatingWaveformSelector.addItem(constants.NOISE)

        self.__statusTextBrowser = self.findChild(QtWidgets.QTextBrowser,'statusTextBrowser')
        self.__statusTextBrowser.setReadOnly(True)
        self.__statusTextBrowser.append(self.__pyVisa.getDeviceStatus())

        self.__checkErrorButton = self.findChild(QtWidgets.QPushButton, 'checkErrorButton')
        self.__checkErrorButton.clicked.connect(self.__pyVisa.checkErrorBus)

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

        self.__nameOfDeviceTextBrowser.clear()
        self.__nameOfDeviceTextBrowser.append(string)

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

        self.__textBrowser.clear()
        self.__textBrowser.append(string)

        self.__nameOfDeviceTextBrowser.clear()
        self.__statusTextBrowser.clear()

        self.__baudRate = baudRate

        self.__configureInstrument()
        if self.__pyVisa.getDeviceStatus() == constants.CONFIGURED:
            self.__pyVisa.getDeviceName(self.__callBackAppendDeviceName)

    def __chooseDeviceWindow(self):
        """Choose device Window

        It's hook for choosing device, from all avalivable connected devices.
        Here we also provide callback which will be invoked after user
        choose device.
        """

        self.__window = ui_ChooseDevice(self.__pyVisa, self.__callBackChooseDevice)

    def __onWaveFormChanged(self, string):
        """On waveform Changed

        That functions is invoked on change waveform event. After changing 
        waveform function changes default data on start.

        Parameters
        ----------
        string :
            information about what is current pick
        """

        if string == constants.DC:
            self.__frequencyLineEdit.setText(constants.DEFAULT)
            self.__amplitudeLineEdit.setText(constants.DEFAULT)
        elif string == constants.NOISE:
            self.__frequencyLineEdit.setText(constants.DEFAULT)
            self.__amplitudeLineEdit.clear()
        else:
            self.__frequencyLineEdit.clear()
            self.__amplitudeLineEdit.clear()

    def __onModulationChanged(self, string):
        """On Modulation Changed

        That functions is invoked on change modulation event. After changing 
        modulation function changes default data on start. Also we switch between
        Deviation parameter and Depth parameter, so we have to change range of valid input
        for one window.

        Parameters
        ----------
        string :
            information about what is current pick
        """

        if string == constants.FM:
            self.__depthDeviationLineEdit.clear()
            regex = QRegExp("(([0-9]{1,8})((\.([0-9]{1,3})))?)")
            inputValidatordepthDeviationLineEdit = QRegExpValidator(regex, self.__depthDeviationLineEdit)
            self.__depthDeviationLineEdit.setValidator(inputValidatordepthDeviationLineEdit)
        elif string == constants.AM:
            self.__depthDeviationLineEdit.clear()
            regex = QRegExp("(([0-9]{1,3}))")
            inputValidatordepthDeviationLineEdit = QRegExpValidator(regex, self.__depthDeviationLineEdit)
            self.__depthDeviationLineEdit.setValidator(inputValidatordepthDeviationLineEdit)

    def __onCheckedOffSet(self):
        """On OffSet checked

        That function is invoked after changing checkbox. After checking on box it allow or disallow to
        enter value for offset. Offset is optional parameter for signal generator.
        """

        if self.__offSetCheckBox.isChecked():
            self.__offsetLineEdit.setStyleSheet("background-color: white; border: 1px outset black;")
            self.__offsetLineEdit.setReadOnly(False)
        else:
            self.__offsetLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
            self.__offsetLineEdit.setReadOnly(True)

    def __onCheckedModulation(self):
        """On Modulation checked

        That function is invoked after changing checkbox. After checking on box it enable modulation for signal.
        It allows to enter values necessary for setting modulation. Also that function manipulate color of box.
        """

        if self.__modulationCheckBox.isChecked():
            self.__frequencyModulationLineEdit.setStyleSheet("background-color: white; border: 1px outset black;")
            self.__frequencyModulationLineEdit.setReadOnly(False)

            self.__depthDeviationLineEdit.setStyleSheet("background-color: white; border: 1px outset black;")
            self.__depthDeviationLineEdit.setReadOnly(False)
        else:
            self.__frequencyModulationLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
            self.__frequencyModulationLineEdit.setReadOnly(True)

            self.__depthDeviationLineEdit.setStyleSheet("background-color: lightgrey; border: lightgrey;")
            self.__depthDeviationLineEdit.setReadOnly(True)

    def __insertToGenerator(self):
        """Function which insert values for signal generator.

        That function insert in proper provided by pyvisa way all data provided by user.
        """
        if self.__pyVisa.getDeviceStatus() == constants.CONFIGURED:
            if self.__checkCorrectness():
                self.__pyVisa.insertWaveform(str(self.__waveFormSelector.currentText()))
                self.__pyVisa.insertFrequency(str(self.__frequencyLineEdit.text()))
                if self.__offSetCheckBox.isChecked():
                    self.__pyVisa.insertAmplitude(str(self.__amplitudeLineEdit.text()), str(self.__offsetLineEdit.text()))
                else:
                    self.__pyVisa.insertAmplitude(str(self.__amplitudeLineEdit.text()))
                if self.__modulationCheckBox.isChecked():
                    self.__pyVisa.insertModulation(str(self.__modulationSelector.currentText()), str(self.__modulatingWaveformSelector.currentText()))
                    self.__pyVisa.insertModulationFreq(str(self.__modulationSelector.currentText()), str(self.__frequencyLineEdit.text()))
                    if self.__modulationSelector.currentText() == constants.FM:
                        self.__pyVisa.insertDeviation(str(self.__depthDeviationLineEdit.text()))
                    elif self.__modulationSelector.currentText() == constants.AM:
                        self.__pyVisa.insertDepth(str(self.__depthDeviationLineEdit.text()))
        else:
            self.errorWindow = ui_ErrorBox(1000000100)

    #selected for refactoring
    def __configureInstrument(self):
        instrumentAddress = self.__textBrowser.toPlainText()
        if instrumentAddress:
            self.__pyVisa.openResource(instrumentAddress)
            if self.__pyVisa.getDeviceStatus() == constants.OPENED:
                self.__pyVisa.configureCommunication(self.__baudRate)
                self.__statusTextBrowser.append(self.__pyVisa.getDeviceStatus())
            else:
                self.__errorWindow = ui_ErrorBox(1000000101)

    #All Values in this function are explained above
    def __checkCorrectness(self):
        if self.__frequencyLineEdit.text():
            if not self.__frequencyLineEdit.text() == constants.DEFAULT:
                if self.__waveFormSelector.currentText() == constants.SINUS:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 15 * float(constants.Mega)):
                        self.__errorWindow = ui_ErrorBox(1100000001)
                        return False
                elif self.__waveFormSelector.currentText() == constants.SQUARE:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 15 * float(constants.Mega)):
                        self.__errorWindow = ui_ErrorBox(1100000002)
                        return False
                elif self.__waveFormSelector.currentText() == constants.RAMP:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 100 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1100000003)
                        return False
                elif self.__waveFormSelector.currentText() == constants.TRIANGLE:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 100 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1100000004)
                        return False
                elif self.__waveFormSelector.currentText() == constants.NOISE:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 15 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1100000005)
                        return False
                elif self.__waveFormSelector.currentText() == constants.DC:
                    if not (float(self.__frequencyLineEdit.text()) >= float(constants.micro) * 100 and float(self.__frequencyLineEdit.text()) <= 15 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1100000006)
                        return False
        else:
            self.__errorWindow = ui_ErrorBox(1000000001)
            return False

        if self.__amplitudeLineEdit.text():
            if not self.__amplitudeLineEdit.text() == constants.DEFAULT:
                if not (float(self.__amplitudeLineEdit.text()) >= float(constants.mili) * 100 and float(self.__amplitudeLineEdit.text()) <= 20):
                    self.__errorWindow = ui_ErrorBox(1000000002)
                    return False
        else:
            self.__errorWindow = ui_ErrorBox(1000000001)
            return False

        #Explanation: |Voffset| + Vpp/2 <= Vmax and |Voffset| <= 2xVpp
        #We have to ensure that both cases are satisfied.
        if self.__offSetCheckBox.isChecked():
            if self.__offsetLineEdit.text():
                if not (abs(float(self.__offsetLineEdit.text())) + float(self.__amplitudeLineEdit.text()) / 2 <= 20 and abs(float(self.__offsetLineEdit.text())) <= 2 * float(self.__amplitudeLineEdit.text())):
                    self.__errorWindow = ui_ErrorBox(1000000003)
                    return False
            else:
                self.__errorWindow = ui_ErrorBox(1000000001)
                return False

        if self.__modulationCheckBox.isChecked():
            if self.__modulationSelector.currentText() == constants.FM:
                if self.__frequencyModulationLineEdit.text():
                    if not (float(self.__frequencyModulationLineEdit.text()) > float(constants.mili) * 10 and float(self.__amplitudeLineEdit.text()) < 10 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1000000004)
                        return False
                else:
                    self.__errorWindow = ui_ErrorBox(1000000001)
                    return False

                if self.__depthDeviationLineEdit.text():
                    if not (float(self.__depthDeviationLineEdit.text()) > float(constants.mili) * 10 and float(self.__depthDeviationLineEdit.text()) < 7.5  * float(constants.Mega)):
                        self.__errorWindow = ui_ErrorBox(1000000005)
                        return False

            elif self.__modulationSelector.currentText() == constants.AM:
                if self.__frequencyModulationLineEdit.text():
                    if not (float(self.__frequencyModulationLineEdit.text()) > float(constants.mili) * 10 and float(self.__amplitudeLineEdit.text()) < 20 * float(constants.kilo)):
                        self.__errorWindow = ui_ErrorBox(1000000006)
                        return False
                else:
                    self.__errorWindow = ui_ErrorBox(1000000001)
                    return False

                if self.__depthDeviationLineEdit.text():
                    if not (float(self.__depthDeviationLineEdit.text()) >= 0 and float(self.__depthDeviationLineEdit.text()) <= 120):
                        self.__errorWindow = ui_ErrorBox(1000000007)
                        return False
        return True