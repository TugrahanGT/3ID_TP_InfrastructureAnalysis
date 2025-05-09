import win32evtlog as WindowsEventLog
import win32con as WindowsConnection
import winerror as WindowsAPIError
import win32evtlogutil as WindowsEventLogUtil
import codecs
import os
import sys
import traceback
from enum import Enum

# Enumeration of the event log types defined in Windows Event Viewer
class EventLogType(Enum):
    Application = 1
    System = 2
    Security = 3

  
event_status_types = {
    WindowsConnection.EVENTLOG_AUDIT_FAILURE:'EVENTLOG_AUDIT_FAILURE',
    WindowsConnection.EVENTLOG_AUDIT_SUCCESS:'EVENTLOG_AUDIT_SUCCESS',
    WindowsConnection.EVENTLOG_INFORMATION_TYPE:'EVENTLOG_INFORMATION_TYPE',
    WindowsConnection.EVENTLOG_WARNING_TYPE:'EVENTLOG_WARNING_TYPE',
    WindowsConnection.EVENTLOG_ERROR_TYPE:'EVENTLOG_ERROR_TYPE'
}  

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
            is provided on {self.timestamp}.\nEvent message is: {self.message}\n"
    
    def get_json_event(self):
        return {
            "ID": self.id,
            "Type": self.type,
            "Source": self.source,
            "Timestamp": self.timestamp,
            "Record": self.record,
            "Message": self.message
        }
    

def readEventLogs(target_name = "localhost", log_type = "Application", log_out_path = os.getcwd() + r"\logs.txt"):    
    event_logs_result = {
        "Errors": {
            "Count": 0,
            "Events": list()
        },
        "Warnings": {
            "Count": 0,
            "Events": list()
        },
        "Informations": {
            "Count": 0,
            "Events": list()
        }
    }

    logging = codecs.open(log_out_path, encoding="utf-8", mode="w")
    line_break = "-" * 80 # For each line, as a separator

    if target_name == "localhost" or log_type == "Application":
        logging.write(f"Either the target name or log type is not provided.\n")
        logging.write(f"By default {target_name} will be used as a target name, and {log_type} will be used as a log type.\n")
    
    logging.write("\n" + line_break + "\n")
    logging.write(f"Logging the {log_type} logs!\n")
    eventLogs = WindowsEventLog.OpenEventLog(target_name, log_type)
    totalNrOfEventLogs = WindowsEventLog.GetNumberOfEventLogRecords(eventLogs)
    logging.write(f"There are {totalNrOfEventLogs} of type {log_type}!\n")
    logging.write("\n" + line_break + "\n")

    flags = WindowsEventLog.EVENTLOG_BACKWARDS_READ | WindowsEventLog.EVENTLOG_SEQUENTIAL_READ
    test_id = 0

    try:
        while True:
            events = WindowsEventLog.ReadEventLog(eventLogs, flags, 0)
            if not events or test_id > 5000:
                break
            for eventObject in events:
                event_timestamp = eventObject.TimeGenerated.Format()
                event_record = eventObject.RecordNumber
                event_message = WindowsEventLogUtil.SafeFormatMessage(eventObject, log_type)
                event_source = str(eventObject.SourceName)
                event_type = event_status_types.get(eventObject.EventType, "Unknown")

                newEventObject = EventObject(test_id, event_type, event_timestamp, event_record, event_source, event_message)


                if event_type == "EVENTLOG_INFORMATION_TYPE":
                    event_logs_result["Informations"]["Count"] = event_logs_result["Informations"]["Count"] + 1
                    event_logs_result["Informations"]["Events"].append(newEventObject.get_json_event())
                elif event_type == "EVENTLOG_WARNING_TYPE":
                    event_logs_result["Warnings"]["Count"] = event_logs_result["Warnings"]["Count"] + 1
                    event_logs_result["Warnings"]["Events"].append(newEventObject.get_json_event())
                elif event_type == "EVENTLOG_ERROR_TYPE":
                    event_logs_result["Errors"]["Count"] = event_logs_result["Errors"]["Count"] + 1
                    event_logs_result["Errors"]["Events"].append(newEventObject.get_json_event())
                
                logging.write(str(newEventObject))
                logging.write("\n" + line_break + "\n")

                test_id = test_id + 1
    except:
        print(traceback.print_exc(sys.exc_info()))

    return event_logs_result