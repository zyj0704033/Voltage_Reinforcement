import logging
import datetime

class Logger(object):
    """docstring for logger."""

    def __init__(self, filename='log_', filedir = './result/log/'):
        super(Logger, self).__init__()
        self.filename = filename
        self.filedir = filedir
        self.time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        self.logger = self.getlogger()


    def getlogger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level = logging.INFO)
        full_filename = self.filedir + self.filename + self.time +'.txt'
        handler = logging.FileHandler(full_filename)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
