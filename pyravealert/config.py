'''
..  codeauthor:: Charles Blais
'''
import logging

from typing import Optional

from enum import Enum

from functools import lru_cache

from pydantic import BaseSettings

import tempfile


class LogLevels(Enum):
    DEBUG: str = 'DEBUG'
    INFO: str = 'INFO'
    WARNING: str = 'WARNING'
    ERROR: str = 'ERROR'


class AppSettings(BaseSettings):
    log_level: LogLevels = LogLevels.WARNING
    log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
    log_datefmt: str = '%Y-%m-%d %H:%M:%S'

    url: str = 'http://localhost'
    username: Optional[str] = None
    password: Optional[str] = None

    ws_port: int = 3000
    ws_write_directory: str = tempfile.gettempdir()

    class Config:
        env_file = '.env'
        env_prefix = 'rave_'

    def configure_logging(self):
        '''
        Configure logging for app
        '''
        level = {
            LogLevels.DEBUG: logging.DEBUG,
            LogLevels.INFO: logging.INFO,
            LogLevels.WARNING: logging.WARNING,
            LogLevels.ERROR: logging.ERROR,
        }[self.log_level]
        logging.basicConfig(
            format=self.log_format,
            datefmt=self.log_datefmt,
            level=level)


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()
