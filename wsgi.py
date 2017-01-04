import cgi
import os, sys
#
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CUR_DIR)

from settings import ServerLogger, MAIN_HANDLER
from WsgiHttp import *
#

def application(environ, start_response):
    try:
        # log activity
        ServerLogger.log_message("> " + environ['REQUEST_METHOD'] + " from " + environ['REMOTE_ADDR'] + ' : ' + environ['PATH_INFO'] + '?' + environ['QUERY_STRING'])
        return MAIN_HANDLER.handle_request(environ, start_response)
    except:
        ServerLogger.log_exception("MAIN")
        return BadHttpResponse(start_response).response()
