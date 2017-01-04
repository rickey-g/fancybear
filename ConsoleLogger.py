import sys

########################################################################

class ConsoleLogger(object):
    def log_exception(self, message=''):
        if message:
            message += " - "
        print "#! EXC: ", message, sys.exc_info()[0].__name__, ":", sys.exc_info()[1]

    def log_error(self, message):
        print "#! ERR:", message

    def log_warning(self, message):
        print "#! WAR:", message

    def log_message(self, message):
        print "#>", message


if __name__ == '__main__':
    logger = ConsoleLogger()
    try:
        raise BaseException("OoooopS! Exception!")
    except:
        logger.log_exception("WTF?!")
    try:
        raise ValueError("OoooopS! Exception! 2")
    except:
        logger.log_exception()
    logger.log_error("Test Error")
    logger.log_warning("Test Warning")
    logger.log_message("Test message")
