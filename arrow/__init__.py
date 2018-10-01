import sys
from webob import Request
from routes import Mapper
import importlib
import time
import threading
import tequilla
import os, os.path

from .application import Application
from .view import View
from .Request import Request
from .Response import Response
from .Object import Object
import arrow.middleware as middleware
import arrow.middleware.auth


class Arrow(object):

    view = View

    url_controllers = {}

    middleware = middleware

    template_handlers = {}

    def __init__(self):
        self.map = Mapper()

    def templates(self, path, name='main'):
        handler = tequilla(os.path.join(os.getcwd(), path))
        handler.compile()
        self.template_handlers[name] = handler
        return handler

    def render(self, template_name, data={}, handler_name='main'):
        return self.template_handlers[handler_name].render(template_name, data)

    def __call__(self):
        return Arrow()

    def run(self, host='localhost', port=8080):
        options = {
            'bind': '%s:%d' % (host, port)
        }
        Application(self.wsgi_app, options).run()

    def route(self, url_template, handler_path):
        module = importlib.import_module(handler_path)
        view = module.View
        self.map.connect(None, url_template, controller=handler_path)
        self.url_controllers[handler_path] = view

    def obj(self, data, name=None):
        o = Object(data)
        if name:
            setattr(self, name, o)
        return o

    def wsgi_app(self, environ, start_response):

        event = threading.Event()

        req = Request(environ)
        res = Response(lambda: event.set())

        route = self.map.match(req.path())
        controller_name = None

        if route:
            controller_name = route.get('controller')

        Handler = self.url_controllers.get(controller_name)

        if Handler:
            thread = threading.Thread(target=Handler(req, res, route).handle)
            thread.daemon = True
            thread.start()
        else:
            res.status(404)

        event.wait()

        start_response(res.status(), res.headerlist())

        return [res.binary()]

sys.modules[__name__] = Arrow()
