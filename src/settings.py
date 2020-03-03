import logging
import pathlib
import sys
from datetime import date
from os import path, makedirs

from src.ctx import Ctx


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = Ctx.request_id.get('request_id')
        return True


log_file_dir = path.join(pathlib.Path(__file__).parent.absolute(), '..', 'server_log')
log_file_path = path.join(log_file_dir, date.today().isoformat() + '-output.log')

if not path.exists(log_file_dir):
    makedirs(log_file_dir)


CUSTOM_LOG_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console", "file"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console", "file"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console", "file"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
            "filters": ['request_id'],
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
            "filters": ['request_id'],
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
            "filters": ['request_id'],
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": log_file_path,
            "mode": "a",
            "filters": ['request_id'],
        }
    },
    filters={
        'request_id': {
            '()': RequestIdFilter,
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] [%(request_id)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                      + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)


