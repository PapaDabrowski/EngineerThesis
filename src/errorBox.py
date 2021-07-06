#Gui imports
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#Internal imports
from errorHandler import errorParser

class ui_ErrorBox(QtWidgets.QWidget):
    """
    Template error box gui class

    That class provides UI which help any other module to print
    error recived from errorParser

    Attributes
    ----------
    errorParser : errorParser
        ErrorParser instance
    confirmButton : QtWidgets.QPushButton
        UI widget button which close window
    textBox : QtWidgets.QLabel
        UI widget label display error

    Methods
    -------
    cancelMethod(self):
        close window function
    """

    def __init__(self, errorCode):
        """Initialization Method

        In init all UI widgets get assigned to hook variables.

        Parameters
        ----------
        errorCode : int
            recived errorCode
        """

        super(ui_ErrorBox, self).__init__()
        self.__errorParser = errorParser()

        uic.loadUi("../UI/errorBar.ui", self)

        self.__confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton')
        self.__confirmButton.clicked.connect(self.cancelMethod)

        self.__textBox = self.findChild(QtWidgets.QLabel, 'label')
        self.__textBox.setText("Error:" + self.__errorParser.printError(errorCode) + "!")
        self.__textBox.setAlignment(Qt.AlignCenter)
        self.__textBox.setWordWrap(True)

        self.show()

    def cancelMethod(self):
        self.close()