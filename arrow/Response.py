import webob
import json


class Response(object):

    def __init__(self, send_callback):
        self.webob_response = webob.Response()
        self._body = ''
        self.send_callback = send_callback

    def send(self, body=None):
        if body:
            self.body(body)
        if self.before_send_mw:
            for mw in self.before_send_mw:
                mw(self)
        self.send_callback()

    def before_send(self, mw):
        if not type(mw) is list:
            mw = [mw]
        self.before_send_mw= mw

    def abort(self, status_code):
        self.status(status_code)
        self.send()

    def ok(self):
        self.status(200)
        self.send()

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

    def binary(self, data=None):
        if not data:
            return self.webob_response.body
        self.webob_response.body = data

    def set_body(self, new_body):
        self._body = new_body
        self.webob_response.text = new_body

    def cookie(self, key, value, **kwargs):
        if not type(value) == str:
            raise TypeError('Cookie value must be string')
        self.webob_response.set_cookie(key, value, **kwargs)

    def delete_cookie(self, *args, **kwargs):
        self.webob_response.delete_cookie(*args, **kwargs)
