class HttpResponse():
    def __init__(self, start_response, status='200 OK', response_body=''):
        self.start_response = start_response
        self.status = status
        self.response_headers = []
        self.response_body = response_body

    def response(self):
        self.response_headers = [('Content-Type','text/plain'), ('Content-Length',str(len(self.response_body)))]
        self.start_response(self.status, self.response_headers)
        return [self.response_body]

class BadHttpResponse(HttpResponse):
    def __init__(self, start_response, error_message='Bad Request'):
        HttpResponse.__init__(self, start_response, '404 BAD', error_message)

########################################################################