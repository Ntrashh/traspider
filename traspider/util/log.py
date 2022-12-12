import platform
import sys
from loguru import logger




class InvalidLogLevelError(Exception):
    pass

class Logging:
    def __init__(self, setting=None):
        """
        """
        spider_name = "TRASPIDER"
        log_write_file = ""
        self.log_level ="INFO".upper()

        if self.log_level not in ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"):
            raise InvalidLogLevelError(self.log_level)

        if self.log_level == "DEBUG":
            logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        else:
            logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <level>{message}</level>"

        if log_write_file:
            handler = {
                    "sink": "logs/%s.log" % spider_name,
                    "rotation": "00:00",
                    "level": self.log_level,
                    "enqueue": True,
                    "colorize": True,
                    "backtrace": False, "diagnose": False,
                    "format": logger_format,
                }
        else:
            handler = {
                "sink": sys.stderr,
                "level": self.log_level,
                "enqueue": True,
                "colorize": True,
                "format": logger_format,
                "backtrace": False, "diagnose": False,
            }

        config = {
            "handlers": [handler]
        }
        logger.configure(**config)

    def get_tb_limit(self):
        if self.log_level == "DEBUG":
            return None
        else:
            return -1


def ignore_windows_close_loop_error():
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise

        return wrapper

    if platform.system() == 'Windows':
        _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


ignore_windows_close_loop_error()