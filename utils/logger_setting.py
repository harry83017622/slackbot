import logging
import logging.config
from datetime import datetime
import datetime as dt
from logging.handlers import SMTPHandler, RotatingFileHandler, TimedRotatingFileHandler
import logging
import re


def get_logger():
    """Get the custom logging"""
    log_format = '[%(processName)s][%(threadName)s]%(asctime)s [%(levelname)s][%(funcName)s]%(message)s'
    date_format = '%m-%d %H:%M'
    log_filename = dt.datetime.now().strftime("./Crawling.log")
    # logging.basicConfig(level=logging.INFO, format='[%(processName)s][%(threadName)s]%(asctime)s [%(levelname)s][%(module)s][%(funcName)s]%(message)s',
    #                     datefmt=date_format)
    handler = TimedRotatingFileHandler(
        log_filename, when='midnight', encoding='utf-8')

    formatter = logging.Formatter(log_format,  datefmt=date_format)
    handler.setFormatter(formatter)
    handler.suffix = '-%Y-%m-%d.log'
    handler.extMatch = re.compile(r"^\d{8}.log$")
    # logging.getLogger().addHandler(handler)
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            handler,
            logging.StreamHandler()
        ]
    )
    # commente first because we need to look
    logging.getLogger('apscheduler.executors.default').propagate = False
    return logging


log = get_logger()