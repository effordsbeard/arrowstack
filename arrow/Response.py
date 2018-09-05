import webob
import json


class Response(webob.Response):

    def __init__(self):
        self.webob_response = webob.Response()
        self._body = ''

    def header(self, name, value=None):
        if value:
            self.webob_response.headers[name] = value
        else:
            return self.webob_response.headers.get(name)

    def headers(self, data=None):
        if data:
            self.webob_response.headers = data
        else:
            return self.webob_response.headers

    def headerlist(self, data=None):
        if data:
            self.webob_response.headerlist = data
        else:
            return self.webob_response.headerlist

    def add(self, data):
        self.set_body(self.body() + data)

    def body(self, data=None):
        if data:
            self.set_body(data)
        else:
            return self.body

    def json(self, data=None):
        if data:
            self.set_body(json.dumps(data))
        else:
            return json.loads(self.body())

    def status(self, data=None):
        if data:
            self.webob_response.status = data
        else:
            return self.webob_response.status

    def status_code(self, data=None):
        if data:
            self.webob_response.status = data
        else:
            return self.webob_response.status_code

    def binary(self):
        return self.webob_response.body

    def set_body(self, new_body):
        self._body = new_body
        self.webob_response.text = new_body
