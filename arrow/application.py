from __future__ import unicode_literals
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems


class Application(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.options['workers'] = (multiprocessing.cpu_count() * 2) + 1 if not options.get('cores_number') else options.get('cores_number')

        self.application = app
        super(Application, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
