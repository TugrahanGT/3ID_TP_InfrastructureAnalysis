import win32evtlog as WindowsEventLog
import win32con as WindowsConnection
import codecs
import logging
from enum import Enum

# Enumeration of the event log types defined in Windows Event Viewer
class EventLogType(Enum):
    Application = 1
    System = 2
    Security = 3

# Enumeration of the event status types defined in Windows Event Viewer
class EventStatusType(Enum):
    WindowsConnection.EVENTLOG_AUDIT_FAILURE = "EVENTLOG_AUDIT_FAILURE"
    WindowsConnection.EVENTLOG_AUDIT_SUCCESS = "EVENTLOG_AUDIT_SUCCESS"
    WindowsConnection.EVENTLOG_INFORMATION_TYPE = "EVENTLOG_INFORMATION_TYPE"
    WindowsConnection.EVENTLOG_WARNING_TYPE = "EVENTLOG_WARNING_TYPE"
    WindowsConnection.EVENTLOG_ERROR_TYPE = "EVENTLOG_ERROR_TYPE"


class EventObject():
    def __init__(self, id, type, timestamp, record, source, message):
        self.id = id
        self.type = type
        self.timestamp = timestamp
        self.record = record
        self.source = source
        self.message = message

    def __str__(self):
        return f"The event with ID: {self.id} and Type: {self.type} from the source {self.source} and record {self.record} \
            is provided on {self.timestamp}.\nEvent message is: {self.message}"
    

def readEventLogs(target_name = "localhost", log_type = "Application"):
    if target_name == "localhost" or log_type == "Application":
        logging.warning("Either the target name or log type is not provided. By default localhost will be used as a target name, and Application will be used as a log type.")

    logging.info(f"Logging the {log_type} logs!")
    eventLogs = WindowsEventLog.OpenEventLog(target_name, log_type)
    totalNrOfEventLogs = WindowsEventLog.GetNumberOfEventLogRecords(eventLogs)
    logging.info(f"There are {totalNrOfEventLogs} of type {log_type}!")

    flags = WindowsEventLog.EVENTLOG_BACKWARDS_READ | WindowsEventLog.EVENTLOG_SEQUENTIAL_READ
    events = WindowsEventLog.ReadEventLog(eventLogs, flags, 0)

    try:
        while True:
            events = WindowsEventLog.ReadEventLog(eventLogs, flags, 0)
            for eventObject in events:
                # @TODO: Implement parser of each event object into the EventObject class
                pass
    except:
        # @TODO: Implement Error Handling
        pass

    return