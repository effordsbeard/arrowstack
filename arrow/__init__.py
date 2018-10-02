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

    def static(self, static_url, static_path):
        self.route(static_url, 'arrow.views.static', view_params={
            'static_path': static_path
        })

    def render(self, template_name, data={}, handler_name='main'):
        return self.template_handlers[handler_name].render(template_name, data)

    def __call__(self):
        return Arrow()

    def run(self, host='localhost', port=8080):
        options = {
            'bind': '%s:%d' % (host, port)
        }
        Application(self.wsgi_app, options).run()

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
