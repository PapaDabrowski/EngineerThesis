#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#Internal imports
from pV import pyVisaInterface

class ui_Osciloscope(QtWidgets.QMainWindow):
    def __init__(self, external, pyVisa):
        super(ui_Osciloscope, self).__init__()
        self.external = external
        self.pyVisa = pyVisa

        if self.external:
            uic.loadUi("../UI/signalGeneratorNested.ui", self)
        else:
            uic.loadUi("../UI/signalGenerator.ui", self)
