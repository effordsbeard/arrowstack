import webob
import json
from copy import deepcopy


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

        if not self.is_json:
            self.data = self.parseargs(self.webob_request.POST)
        else:
            self._json = self.json()

        self._params = {**self.query, **self.data}

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

    def header(self, name, placeholder=None):
        return self.webob_request.headers.get(name, placeholder)

    def json(self):
        try:
             if not self._json:
                 self._json = json.loads(self.webob_request.body)
        except:
            self._json = {}

        return self._json

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
