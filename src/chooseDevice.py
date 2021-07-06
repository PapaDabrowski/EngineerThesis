import sys

#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator

#Internal imports
from pV import pyVisaInterface

class ui_ChooseDevice(QtWidgets.QMainWindow):
    def __init__(self, pyVisa, callBack):
        super(ui_ChooseDevice, self).__init__()
        self.__pyVisa = pyVisa
        self.__callBack = callBack

        uic.loadUi("../UI/choosePanel.ui", self)

        self.__listWidget = self.findChild(QtWidgets.QListWidget, 'listWidget')

        self.__lineEditBaudRate = self.findChild(QtWidgets.QLineEdit,'lineEditBaudRate')
        regex = QRegExp("[0-9]{3,7}")
        inputValidator = QRegExpValidator(regex, self.lineEditBaudRate)
        self.__lineEditBaudRate.setValidator(inputValidator)

        self.__confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton')
        self.__confirmButton.clicked.connect(self.__confirmMethod)

        self.__cancelButton = self.findChild(QtWidgets.QPushButton, 'cancelButton')
        self.__cancelButton.clicked.connect(self.__cancelMethod)

        self.__loadItemsToList()

        self.show()

    def __loadItemsToList(self):
        for x in self.__pyVisa.listOfResources():
            item = QListWidgetItem(x)
            self.__listWidget.addItem(item)

    def __confirmMethod(self):
        if self.__listWidget.currentItem() is None:
            self.__cancelMethod()
        else:
            self.__callBack(self.__listWidget.currentItem().text(), self.__lineEditBaudRate.text())
            self.__cancelMethod()

    def __cancelMethod(self):
        self.close()