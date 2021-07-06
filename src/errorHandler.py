class errorParser:
    """
    ErrorParser class which basicly translates errorCodes to string explained value

    Methods
    -------
    printError(self, statusCode):
        function which translate error code to explanatory string
    """

    def __init__(self):
        """Initialization Method

        """

        pass

    def printError(self, statusCode):
        """Function which parse errorCode

        Parameters
        ----------
        statusCode : int
            Error code

        Returns
        -------
        string
            Parsed human-readable string
        """

        self.__choices = {
            -1073807312 : 'The operation was aborted.',
            -1073807300 : 'Insufficient system resources to perform necessary memory allocation.',
            -1073807329 : 'The specified attribute is read-only.',
            -1073807304 : 'Bus error occurred during transfer.',
            -1073807338 : 'Unable to deallocate the previously allocated data structures corresponding to this session or object reference.',
            -1073807194 : 'The connection for the specified session has been lost.',
            -1073807199 : 'An error occurred while trying to open the specified file.Possible causes include an invalid path or lack of access rights.',
            -1073807198 : 'An error occurred while performing I/O on the specified file.',
            -1073807320 : 'A handler is not currently installed for the specified event.',
            -1073807303 : 'Unable to queue the asynchronous operation because there is already an operation in progress.',
            -1073807305 : 'Device reported an input protocol error during transfer.',
            -1073807195 : 'The interface type is valid but the specified interface number is not configured.',
            -1073807256 : 'An interrupt is still pending from a previous call.',
            -1073807327 : 'The access key to the resource associated with this session is invalid.',
            -1073807341 : 'Invalid access mode.',
            -1073807282 : 'Invalid address space specified.',
            -1073807333 : 'Specified degree is invalid.',
            -1073807322 : 'Specified event type is not supported by the resource.',
            -1073807344 : 'Invalid expression specified for search.',
            -1073807297 : 'A format specifier in the format string is invalid.',
            -1073807319 : 'The specified handler reference is invalid.',
            -1073807332 : 'Specified job identifier is invalid.',
            -1073807229 : 'Invalid length specified.',
            -1073807200 : 'The value specified by the line parameter is invalid.',
            -1073807328 : 'The specified type of lock is not supported by this resource.',
            -1073807299 : 'Invalid buffer mask specified.',
            -1073807321 : 'Invalid mechanism specified.',
            -1073807215 : 'The specified mode is invalid.',
            -1073807346 : 'The specified session or object reference is invalid.',
            -1073807279 : 'Invalid offset specified.',
            -1073807240 : 'The value of an unknown parameter is invalid.',
            -1073807239 : 'The protocol specified is invalid.',
            -1073807342 : 'Invalid resource reference specified. Parsing error.',
            -1073807302 : 'Unable to start operation because setup is invalid due to inconsistent state of properties.',
            -1073807237 : 'Invalid size of window specified.',
            -1073807278 : 'Invalid source or destination width specified.',
            -1073807298 : 'Could not perform operation because of I/O error.',
            -1073807202 : 'A code library required by VISA could not be located or loaded.',
            -1073807294 : 'The specified trigger line is currently in use.',
            -1073807193 : 'The remote machine does not exist or is not accepting any connections.',
            -1073807203 : 'The device does not export any memory.',
            -1073807265 : 'No listeners condition is detected (both NRFD and NDAC are deasserted).',
            -1073807192 : 'Access to the remote machine is denied.',
            -1073807231 : 'The specified operation is unimplemented.',
            -1073807331 : 'The specified attribute is not defined or supported by the referenced session, event, or find list.',
            -1073807330 : 'The specified state of the attribute is not valid or is not supported as defined by the session, event, or find list.',
            -1073807295 : 'A format specifier in the format string is not supported.',
            -1073807201 : 'The interface cannot generate an interrupt on the requested level or with the requested statusID value.',
            -1073807197 : 'The specified trigger source line (trigSrc) or destination line (trigDest) is not supported by this VISA implementation, or the combination of lines is not a valid mapping.',
            -1073807196 : 'The specified mechanism is not supported for the specified event type.',
            -1073807290 : 'The specified mode is not supported by this VISA implementation.',
            -1073807276 : 'Specified offset is not accessible from this hardware.',
            -1073807248 : 'The specified offset is not properly aligned for the access width of the operation.',
            -1073807257 : 'The session or object reference does not support this operation.',
            -1073807275 : 'Cannot support source and destination widths that are different.',
            -1073807242 : 'Specified width is not supported by this hardware.',
            -1073807264 : 'The interface associated with this session is not currently the Controller-in-Charge.',
            -1073807313 : 'The session must be enabled for events of the specified type in order to receive them.',
            -1073807263 : 'The interface associated with this session is not the system controller.',
            -1073807306 : 'Device reported an output protocol error during transfer.',
            -1073807301 : 'Unable to queue asynchronous operation.',
            -1073807315 : 'The event queue for the specified type has overflowed, usually due to not closing previous events.',
            -1073807307 : 'Violation of raw read protocol occurred during transfer.',
            -1073807308 : 'Violation of raw write protocol occurred during transfer.',
            -1073807246 : 'The resource is valid, but VISA cannot currently access it.',
            -1073807345 : 'Specified type of lock cannot be obtained or specified operation cannot be performed because the resource is locked.',
            -1073807343 : 'Insufficient location information, or the device or resource is not present in the system.',
            -1073807271 : 'A previous response is still pending, causing a multiple query error.',
            -1073807253 : 'A framing error occurred during transfer.',
            -1073807252 : 'An overrun error occurred during transfer. A character was not read from the hardware before the next character arrived.',
            -1073807254 : 'A parity error occurred during transfer.',
            -1073807204 : 'The current session did not have any lock on the resource.',
            -1073807286 : 'Service request has not been received for the session.',
            -1073807360 : 'Unknown system error.',
            -1073807339 : 'Timeout expired before operation completed.',
            -1073807250 : 'The path from the trigger source line (trigSrc) to the destination line (trigDest) is not currently mapped.',
            -1073807247 : 'A specified user buffer is not valid or cannot be accessed for the required size.',
            -1073807232 : 'The specified session currently contains a mapped window.',
            -1073807273 : 'The specified session is currently unmapped.',
            0 : 'Operation completed successfully.',
            1000000000 : 'Parsing errors:',
            1000000001 : 'Please insert all necessary values',
            1000000002 : 'Amplitude have to be from 100 mVpp up to 20 Vpp for open circuit',
            1000000003 : 'OffsetValue have to be in range of this def: |Voffset| + Vpp/2 <= Vmax and |Voffset| <= 2xVpp',
            1000000004 : 'Modulating FM frequency have to be any value between 10 mHz and 10 kHz',
            1000000005 : 'Deviation for FM modulation have to be any value between 10 mHz and 7.5 MHz',
            1000000006 : 'Modulating AM frequency have to be any value between 10 mHz and 10 kHz',
            1000000007 : 'Depth for AM modulation have to be any value between 0% and 120%',
            1000000100 : 'Device is disconnected',
            1000000101 : 'Cannot open the device, check connection and try again',
            1073676413 : 'Session opened successfully, but the device at the specified address is not responding.',
            1073676291 : 'Specified event is already disabled for at least one of the specified mechanisms.',
            1073676290 : 'Specified event is already enabled for at least one of the specified mechanisms.',
            1073676294 : 'The number of bytes read is equal to the input count.',
            1073676442 : 'Operation completed successfully, and this session has nested exclusive locks.',
            1073676441 : 'Operation completed successfully, and this session has nested shared locks.',
            1073676440 : 'Event handled successfully. Do not invoke any other handlers on this session for this event.',
            1073676292 : 'Operation completed successfully, but the queue was already empty.',
            1073676416 : 'Wait terminated successfully on receipt of an event notification. There is still at least one more event occurrence of the requested type(s) available for this session.',
            1073676443 : 'Asynchronous operation request was performed synchronously.',
            1073676293 : 'The specified termination character was read.',
            1073676414 : 'The path from the trigger source line (trigSrc) to the destination line (trigDest) is already mapped.',
            1073676407 : 'The specified configuration either does not exist or could not be loaded.The VISA-specified defaults are used.',
            1073676457 : 'The operation succeeded, but a lower level driver did not implement the extended functionality.',
            1073676420 : 'Although the specified state of the attribute is valid, it is not supported by this resource implementation.',
            1073676424 : 'The specified buffer is not supported.',
            1073676418 : 'The specified object reference is uninitialized.',
            1073676300 : 'VISA received more event information of the specified type than the configured queue size could hold.',
            1073676421 : 'The status code passed to the operation could not be interpreted.',
            1100000001 : 'Frequency for Sine have to be any value between 100 uHz up to 15 MHz',
            1100000002 : 'Frequency for Square have to be any value between 100 uHz up to 15 MHz',
            1100000003 : 'Frequency for Ramp have to be any value between 100 uHz up to 100 kHz',
            1100000004 : 'Frequency for Triangle have to be any value between 100 uHz up to 100 kHz',
            1100000005 : 'Frequency for Noise have to be any value between 100 uHz up to 100 kHz ???? or set to DEFault',
            1100000006 : 'Frequency for DC have to be any value between 100 uHz up to 100 kHz ??? or set to DEFault',
            9999999999 : 'Not implemented in this release version'
            }
        return self.__choices.get(statusCode, 'Ocurred Error not found ErrorCode="%d" ' % (statusCode))