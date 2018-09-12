import sys
from webob import Request
from routes import Mapper
import importlib
import time
import threading

from .application import Application
from .view import View
from .Request import Request
from .Response import Response
import arrow.middleware as middleware
import arrow.middleware.auth


class Arrow(object):

    view = View

    url_controllers = {}

    middleware = middleware

    def __init__(self):
        self.map = Mapper()
        # self.map.connect(None, "/error/{action}/{id}", controller="error")
        # self.map.connect("home", "/", controller="main", action="index")

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
