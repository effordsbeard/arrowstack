import webob
import json
from copy import deepcopy
from .File import File
import urllib.parse as urlp
from .Object import Object


import cgi

class Request(object):

    data = {}
    query = {}
    _params = {}

    _json = None

    def __init__(self, environ):
        self.environ = environ
        self.webob_request = webob.Request(environ)

        self.is_json = True if self.header('Content-Type') == 'application/json' else False

        self.query = self.parseargs(self.webob_request.GET)
        self.files = {}

        if not self.is_json:
            self.data = self.parseargs(self.webob_request.POST)
        else:
            self._json = self.json()

        self._params = {**self.query, **self.data}

        for name, field in self.data.items():
            if isinstance(field, cgi.FieldStorage):
                if '/' in field.filename:
                    continue
                self.files[name] = File(field)

    def referer(self, parse=False):
        if parse:
            if not hasattr(self, '_referer'):
                r = urlp.urlparse(self.header('Referer'))
                q = urlp.parse_qs(r.query)
                p = r.path
                self._referer = Object({
                    'hostname': r.hostname,
                    'query': dict(q),
                    'path': p
                }, recursive=False)
            return self._referer
        return self.header('Referer')

    def method(self):
        return self.webob_request.method

    def path(self):
        return self.webob_request.path

    def params(self):
        return self._params

    def param(self, name, value=None):
        if not value:
            return self._params.get(name)
        else:
            self._params[name] = value

    def file(self, name):
        return self.files.get(name, None)

    def header(self, name, placeholder=None):
        return self.webob_request.headers.get(name, placeholder)

    def headers(self):
        return self.webob_request.headers

    def ip(self):
        return self.webob_request.client_addr

    def ua(self):
        return self.webob_request.user_agent

    def url(self):
        return self.webob_request.url

    def domain(self):
        return self.webob_request.domain

    def host(self):
        return self.webob_request.host

    def port(self):
        return self.webob_request.host_port

    def query_string(self):
        return self.webob_request.query_string

    def query(self):
        return self.webob_request.GET

    def post(self):
        return self.webob_request.POST

    def json(self):
        try:
             if not self._json:
                 self._json = json.loads(self.webob_request.body)
        except:
            self._json = {}

        return self._json

    def text(self, data=None):
        if data:
            self.webob_request.text = data
        else:
            return self.webob_request.text

    def body(self, data=None):
        if data:
            self.webob_request.body = data
        else:
            return self.webob_request.body

    def cookie(self, key):
        return self.webob_request.cookies.get(key)

    def parseargs(self, args):
        _a = {}
        for key, value in args.items():
            _key = key.replace(']', '').split('[')
            if len(_key) == 2:
                main_key = _key[0]
                index_key = _key[1]
                if not main_key in _a:
                    if index_key:
                        _a[main_key] = dict()
                    else:
                        _a[main_key] = list()

                if index_key:
                    _a[main_key][index_key] = value
                else:
                    _a[main_key].append(value)

            elif len(_key) == 1:
                _key = key
                if len(args.getall(key)) == 1:
                    _a[key] = value
                else:
                    if not _key in _a:
                        _a[_key] = list()
                    _a[_key].append(value)
            else:
                print('Incorrect format of arg:', key, value)
        return _a
