import webob

class Request(object):

    def __init__(self, environ):
        self.webob_request = webob.Request(environ)

    def method(self):
        return self.webob_request.method

    def path(self):
        return self.webob_request.path

    def params(self):
        return self.webob_request.params

    def param(self, name, placeholder=None):
        return self.webob_request.params.get(name, placeholder)

    def header(self, name, placeholder=None):
        return self.webob_request.headers.get(name, placeholder)
