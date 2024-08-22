from enum import Enum


class Level(Enum):
    EMPTY = "empty"
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    NOTICE = "notice"
    CAUTION = "caution"
    ERROR = "error"
    CRITICAL = "critical"
    EMERGENCY = "emergency"
