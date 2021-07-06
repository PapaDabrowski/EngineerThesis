from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator

from pV import pyVisaInterface
import constants

from chooseDevice import ui_ChooseDevice
from signalGenerator import ui_SignalGenerator
from errorBox import ui_ErrorBox
from osciloscope import ui_Osciloscope
from multimeter import ui_Multimeter
from mainWindow import ui_MainWindow

import sys

app = QtWidgets.QApplication(sys.argv)

window = ui_MainWindow('@sim')

app.exec()