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
import arrow.views
from .mime import MIME


class Arrow(object):

    view = View

    mime = MIME

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

    def static(self, static_url, static_path, exclude=[]):
        self.route(static_url, 'arrow.views.static', view_params={
            'static_path': static_path,
            'exclude': exclude
        })

    def file(self, path):
        try:
            with open(path, 'rb') as f:
                return f.read()
        except:
            raise IOError('File not found:', path)

    def get_mime(self, path):
        filename, ext = os.path.splitext(path)
        return self.mime.get(ext)

    def render(self, template_name, data={}, handler_name='main'):
        return self.template_handlers[handler_name].render(template_name, data)

    def __call__(self):
        return Arrow()

    def run(self, options={}):
        _options = {
            'bind': '%s:%d' % (options.get('host', 'localhost'), options.get('port', 8080))
        }
        _options.update(options)
        Application(self.wsgi_app, _options).run()

    def route(self, url_template, handler_path, view_params={}):
        module = importlib.import_module(handler_path)
        view = module.View
        self.map.connect(None, url_template, controller=handler_path)
        self.url_controllers[handler_path] = {
            'view': view,
            'params': view_params
        }

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

        view = self.url_controllers.get(controller_name)

        if not view:
            res.status(404)
        else:
            Handler = view.get('view')
            view_params = view.get('params')
            thread = threading.Thread(target=Handler(req, res, route, params=view_params).handle)
            thread.daemon = True
            thread.start()
            event.wait()

        start_response(res.status(), res.headerlist())

        return [res.binary()]

sys.modules[__name__] = Arrow()
