import logging

def get_logger(name):
    FORMAT = '%(asctime)-15s %(name)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(name)
    return logger

class AwesomeClassBase(object):
    """docstring for class AwesomeClassBase(object):"""

    def __init__(self, *args, **kwargs):
        self.logger = get_logger('l0-base')
        super(AwesomeClassBase, self).__init__()
        for key, value in kwargs.items():
              setattr(self, key, value)