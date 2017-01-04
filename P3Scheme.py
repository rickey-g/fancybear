import XABase64
class P3Scheme(object):
    def __init__(self, private_token, service_token, xor_part_length=4):
        self.private_token = private_token
        self.service_token = service_token
        self.xor_part_length = xor_part_length
        self.separator = '&&'

    def pack_service_data(self, data):
        return XABase64.pack(data, self.service_token)

    def pack_data(self, data):
        return XABase64.pack(data, self.private_token)

    def pack_agent_data(self, data):
        return XABase64.pack_xor_part(data, self.private_token, self.xor_part_length)

    def unpack_service_data(self, data):
        return XABase64.unpack(data, self.service_token)

    def unpack_data(self, data):
        return XABase64.unpack(data, self.private_token)

    def unpack_agent_data(self, data):
        return XABase64.unpack_xor_part(data, self.private_token, self.xor_part_length)

if __name__ == '__main__':
    P3_PRIVATE_TOKEN = '\xd2\x0e\x25\xf9\x11\x31\x24'
    P3_SERVICE_TOKEN = '\x01\x5a\x13\x54\xac\xf1\xb1'
    #
    P3_Scheme = P3Scheme(private_token=P3_PRIVATE_TOKEN, service_token=P3_SERVICE_TOKEN)
    #
    # Test meta info decode
    d = ['vPjiWMxpiMOEUR8kiK0ZgfEk2FhUoUgEBN1MAHipbZAMsWAIHIFIBHSpaAwoqUBYVK1UCHStUHgIjTAEAKA==',
         'UfPg7lMrz8kbE1guF-9e10Z7V1Kb6wsC5-8PfpPOnwqLwwcSu_8rcpPvLxKD71dSl_cHcpfzdw63kwsGm',
         '5EKRq1p5mhASQQ33Hr0LDk8pAouSuV7b7r1ap5qcytOCkU7Tsr1Kq4KhUve-sQKLnqVSq56hIte-wV7fk',
         'jd0rlgyP86VEt2RCSEtiuxnfaz7ETzduuEszEshOo2bQZzdi5EcTHsBvM0Lca2s-yGs7HshXEx7ITzMex[']
    for i in d:
        print P3_Scheme.unpack_data(i)
        #print XABase64.unpack_xor_part(i, P3_PRIVATE_TOKEN, 0)
