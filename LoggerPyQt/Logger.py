import logging
import logging.handlers
# from PyQt5.Qax import Qweb

class loggerTimeRotate():
    def __init__(self, loggerName, level=logging.INFO):
        self.loggerName = loggerName
        self.level = level
        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d:%(message)s')
        self.handler = logging.handlers.RotatingFileHandler("timeRotateFile", 'M', 1, 0)
        self.handler.suffix = "%Y%m%d-%H%M.log"
        self.handler.setFormatter(formatter)

    def getLogger(self):
        logger = logging.getLogger(self.loggerName)
        logger.setLevel(self.level)
        logger.addHandler(self.handler)
        return logger


class loggerFile():
    def __init__(self, loggerName, level=logging.INFO):
        self.loggerName = loggerName
        self.level = level
        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s Line:%(lineno)d:%(message)s')
        self.handler = logging.FileHandler("filetest.log")
        self.handler.setFormatter(formatter)

    def getLogger(self):
        logger = logging.getLogger(self.loggerName)
        logger.setLevel(self.level)
        logger.addHandler(self.handler)
        return logger