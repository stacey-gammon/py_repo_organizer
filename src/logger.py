import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

class Logger:
    def __init__(self, log_level: LogLevel) -> None:
        self.log_level: LogLevel = log_level

    def log(self, level: LogLevel, message: str) -> None:
        if self.log_level.value <= level.value:
            level_str = (
                "DEBUG" if level.value == LogLevel.DEBUG.value else
                "INFO" if level.value == LogLevel.INFO.value else
                "WARN" if level.value == LogLevel.WARN.value else "ERROR")
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{level_str}] {timestamp} {message}")

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warn(self, message: str) -> None:
        self.log(LogLevel.WARN, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)
