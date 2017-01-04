import sys, os
from datetime import datetime

os.umask(0000)

########################################################################

class FileConsoleLogger(object):
    def __init__(self, log_file):
        self.log_file = log_file
        self.save_log("### Started " + datetime.utcnow().isoformat() + "\n")

    def save_log(self, log):
        f = open(self.log_file, "a")
        f.write(log)
        f.flush()
        f.close()

    def log_exception(self, message=''):
        if message:
            message += " - "
        log = "".join( ("#! EXC: ", message, sys.exc_info()[0].__name__, ":", str(sys.exc_info()[1]) ) )
        print log
        self.save_log( datetime.utcnow().isoformat() + " " + log + "\n" )

    def log_error(self, message):
        log =  "".join( ("#! ERR: ", message) )
        print log
        self.save_log( datetime.utcnow().isoformat() + " " + log + "\n" )

    def log_warning(self, message):
        log =  "".join( ("#! WAR: ", message) )
        print log
        self.save_log( datetime.utcnow().isoformat() + " " + log + "\n" )

    def log_message(self, message):
        log =  " ".join( ("#>", message) )
        print log

########################################################################

if __name__ == '__main__':
    logger = FileConsoleLogger("_log.log")
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
