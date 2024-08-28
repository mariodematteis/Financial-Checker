from dataclasses import dataclass

from financialchecker.log.models import LogType


@dataclass
class Log:
    """
    Data class representing a log entry.

    Attributes:
        PackageName (str): Name of the package related to the log entry.
        ModuleName (str): Name of the module related to the log entry.
        Level (LogType): Log level indicating the severity of the log entry.
        Message (str): Log message providing information or details.
    """

    PackageName: str
    ModuleName: str
    Level: LogType
    Message: str
