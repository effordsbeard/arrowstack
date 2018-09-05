import sys
from webob import Request
from routes import Mapper
import importlib

from .application import Application
from .view import View
from .Request import Request
from .Response import Response
import arrow.middleware as middleware

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
        view = module.View()
        self.map.connect(None, url_template, controller=handler_path)
        self.url_controllers[handler_path] = view

    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        res = Response()

        handler_name = self.map.match(req.path())
        controller_name = None

        if handler_name:
            controller_name = handler_name.get('controller')

        handler = self.url_controllers.get(controller_name)

        if handler:
            handler.handle(req, res)
        else:
            res.status(404)

        start_response(res.status(), res.headerlist())

        return [res.binary()]

sys.modules[__name__] = Arrow()
