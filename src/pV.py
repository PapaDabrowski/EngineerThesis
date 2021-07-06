import re
import time
import math
import inspect
from datetime import datetime

import pyvisa
from pyvisa import constants

#Internal imports
import constants
from errorHandler import errorParser
from errorBox import ui_ErrorBox

class pyVisaInterface:
    """
    pyVisaInterface, wrapper for pyVisa library

    Class provides API like methods to manage measurement devices for GUI classes.

    Attributes
    ----------

    Methods
    -------
    listOfResource(self):touple
        returns list of avalivables devices
    openResource(self,string):
        opens selected device
    getDeviceStatus(self) : string
        returns state of pyVisa about connections
    getDeviceName(self,callback):
        returns device name
    configureCommunication(self, baud_rate):
        configurate communications with device
    insertWaveform(self,waveform):
        inserting selected waveform into device
    insertFrequency(self, frequency):
        inserting selected frequency into device
    insertAmplitude(self, amplitude, offSet ):
        inserting selected amplitude into device
    insertModulation(self, modulation, waveform):
        inserting selected modulation into device
    insertModulationFreq(self, modulation, frequency):
        inserting selected frequency of modulation into device
    insertDeviation(self, deviation):
        inserting deviation of modulation into device
    insertDepth(self, depth):
        inserting Depth of modulation into device
    """

    def __init__(self, type, logOutput):
        self.__resourceManager = pyvisa.ResourceManager(type)
        self.__logOutput = logOutput
        self.__errorParser = errorParser()
        self.__state = constants.DISCONNECTED

#Generic functions

    def listOfResources(self):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        caller = self.__convertCallerToPrev('{}'.format(the_class))

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S - ")
        try:
            return self.__resourceManager.list_resources()
        except pyvisa.errors.VisaIOError as error:
            self.__logOutput.addItem(current_time + caller + '{}'.format(error))
            self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))

    def openResource(self, string):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        caller = self.__convertCallerToPrev('{}'.format(the_class))

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S - ")
        try:
            self.__instrument = self.__resourceManager.open_resource(string)
            self.__state = constants.OPENED
        except pyvisa.errors.VisaIOError as error:
            self.__state = constants.ERROR
            self.__logOutput.addItem(current_time + caller + '{}'.format(error))
            self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))

    def getDeviceStatus(self):
        return self.__state

    def getDeviceName(self, callback):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                infoTemp = self.__instrument.query('*IDN?', delay=0.1)
                callback(infoTemp)
            except pyvisa.errors.VisaIOError as error:
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def configureCommunication(self, baud_rate):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                self.__instrument.write('*RST')
                self.__instrument.write('*CLS')

                self.__instrument.baud_rate = int(baud_rate)
                self.__instrument.read_termination = '\n'
                self.__instrument.write_termination = '\n'
                infoTemp = self.__instrument.query('*IDN?', delay=0.1)

                #LogOutput probalby temporary, so far very usefull for debug purposes
                self.__logOutput.addItem(current_time + caller + 'baud_rate = ' + baud_rate)
                self.__logOutput.addItem(current_time + caller + '*IDN?')
                self.__logOutput.addItem(current_time + caller + infoTemp)
                self.__state = constants.CONFIGURED
            except pyvisa.errors.VisaIOError as error:
                self.__state = constants.ERROR
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

#Signal Generator

    def insertWaveform(self, waveform):
        if not self.__state == constants.DISCONNECTED:
            temp = 'FUNC:SHAP' + ' ' + self.__constToInputString(waveform)
            self.__instrument.write(temp)
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertFrequency(self, frequency):
        if not self.__state == constants.DISCONNECTED:
            temp = 'FREQ' + ' ' + frequency
            self.__instrument.write(temp)
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertAmplitude(self, amplitude, offSet = ''):
        if not self.__state == constants.DISCONNECTED:
            temp = 'VOLT' + ' ' + amplitude
            self.__instrument.write(temp)
            if offSet:
                temp = 'VOLT:OFFS' + ' ' + offSet
                self.__instrument.write(temp)
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertModulation(self, modulation, waveform):
        if not self.__state == constants.DISCONNECTED:
            if modulation == constants.AM:
                temp = 'AM:INT:FUNC' + ' ' + self.__constToInputString(waveform)
            elif modulation == constants.FM:
                temp = 'FM:INT:FUNC' + ' ' + self.__constToInputString(waveform)
            self.__instrument.write(temp)
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertModulationFreq(self, modulation, frequency):
        if not self.__state == constants.DISCONNECTED:
            if modulation == constants.AM:
                temp = 'AM:INT:FREQ' + ' ' + frequency
            elif modulation == constants.FM:
                temp = 'FM:INT:FREQ' + ' ' + frequency
            self.__instrument.write(temp)
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertDeviation(self, deviation):
        if not self.__state == constants.DISCONNECTED:
            temp = 'FM:DEV' + ' ' + deviation
            self.__instrument.write(temp)
            self.__instrument.write('FM:STAT ON')
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def insertDepth(self, depth):
        if not self.__state == constants.DISCONNECTED:
            temp = 'AM:DEPT' + ' ' + depth
            self.__instrument.write(temp)
            self.__instrument.write('AM:STAT ON')
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def checkErrorBus(self):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                temp = self.__instrument.query('SYST:ERR?')
                if temp:
                    self.__logOutput.addItem(temp)
            except pyvisa.errors.VisaIOError as error:
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def checkWaveform(self, waveform):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                temp = self.__instrument.query('FUNC:SHAP?')
                if temp == self.__constToInputString(waveform):
                    return True
                return False
            except pyvisa.errors.VisaIOError as error:
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

    def checkFrequency(self, frequency):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                temp = self.__instrument.query_ascii_values('FREQ?')
                if math.isclose(self.__convertToFloat(temp), frequency, abs_rel = 1e-09, abs_tol = 0.1):
                    return True
                return False
            except pyvisa.errors.VisaIOError as error:
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

#Multimeter

    def autoMeasure(self, string):
        if not self.__state == constants.DISCONNECTED:
            stack = inspect.stack()
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            caller = self.__convertCallerToPrev('{}'.format(the_class))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S - ")
            try:
                self.__instrument.query_ascii_values(self.__constToInputString(constants.MEASURE + ':' + string) + '? DEF,DEF')
                return temp
            except pyvisa.errors.VisaIOError as error:
                self.__logOutput.addItem(current_time + caller + '{}'.format(error))
                self.__errorWindow = ui_ErrorBox(self.__extractValueFromString('{}'.format(error)))
        else:
            self.__errorWindow = ui_ErrorBox(1000000100)

#Helper functions

    def __constToInputString(self, string):
        return ''.join(c for c in string if c.isupper() or c == ':')

    def __convertToFloat(self, value):
        return float(value)

    def __extractValueFromString(self, string):
        return int(''.join(i for i in string if i.isdigit() or i == "-"))

    def __convertCallerToPrev(self, string):
        if string == 'ui_SignalGenerator':
            return 'signalGen: '
        elif string == 'ui_Multimeter':
            return 'multimerer: '

    def __clearDevice(self):
        self.__instrument.query("status:measurement?")
        self.__instrument.write("trace:clear; trace:feed:control next")

    def __handleEvent(self, resource, event, user_handle):
        resource.called = True;
        self.__logOutput.addItem("Handled event {event.event_type} on {resource}")
        self.__instrument.called = False;
        
        # Type of event we want to be notified about
        #event_type = constants.EventType.service_request
        
        # Mechanism by which we want to be notified
        #event_mech = constants.EventMechanism.queue
        
        wrapped = __instrument.wrap_handler(handle_event)

        user_handle = __instrument.install_handler(event_type, wrapped, 42)
        __instrument.enable_event(event_type, event_mech, None)

        # __instrument specific code to enable service request
        # (for example on operation complete OPC)
        __instrument.write("*SRE 1")
        __instrument.write("INIT")

        while not __instrument.called:
            sleep(2)

        __instrument.disable_event(event_type, event_mech)
        __instrument.uninstall_handler(event_type, wrapped, user_handle)
