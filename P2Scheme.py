import struct
import base64
import XABase64


class P2SchemeException(BaseException):
    pass

class P2Scheme(object):
    # | b64junk [5] |                  xb64data                  |
    # |             |             UrlSafe_Base64(...)            |
    # |             | binary_junk [4] |    XORed with bin_junk   |
    # |                               | token [7] | data [...]   |

    def __init__(self, _url_token, _data_token, _subj_token, _mark='ai=', _b64junk_len=9, _binary_junk_len=4, _xor_part_length=4):
        self.url_token = _url_token
        self.data_token = _data_token
        self.subj_token = _subj_token
        self.mark = _mark
        self.b64junk_len = _b64junk_len
        self.binary_junk_len = _binary_junk_len
        self.xor_part_length = _xor_part_length

    '''def parse_query(self, query_string):
        mark = self.mark
        data = None
        aid_len = 4
        mark_size = len(mark)
        mark_position = query_string.find(mark)
        if mark_position == -1:
            raise P2SchemeException("Incorrect url format(1)!")
        params = query_string.split('&')
        for param in params:
            if param[:mark_size] == mark:
                data = param[mark_size:]
                break
        if len(data) < len(self.url_token) + aid_len:
            raise P2SchemeException("Parse query error! Incorrect data length!")
        return data

    def parse_url(self, path, query_string):
        data = self.parse_query(query_string)
        aid = XABase64.unpack(data, self.url_token)
        try:
            aid = struct.unpack("<I", aid)[0]
        except:
            raise P2SchemeException("Incorrect AID data length!")
        return aid'''

    def pack_data(self, data):
        return XABase64.pack(data, self.data_token)

    def unpack_data(self, data):
        return XABase64.unpack(data, self.data_token)

    def pack_agent_data(self, data):
        return XABase64.pack_xor_part(data, self.data_token, self.xor_part_length)

    def unpack_agent_data(self, data):
        return XABase64.unpack_xor_part(data, self.data_token, self.xor_part_length)

    # Tests
    def generate_test_url(self, aid):
        data = XABase64.pack( struct.pack("<I", aid), self.url_token )
        url = '/hwnd/1/?q=234&hl=eN&' + self.mark + data + '&autc=120846146670'
        return url

