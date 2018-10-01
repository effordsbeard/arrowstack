from webob import Response
import re


methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

class View(object):

    allow_unrecognized = True
    params = {}
    json = None
    json_maxlevel = 10
    middleware = []
    after_middleware = []

    def __init__(self, req, res, route):
        self.req = req
        self.res = res
        self.res.before_send(self.after_middleware)
        self.route = route

    def handle(self):
        if not self.validate():
            return self.res.abort(400)

        if self.middleware:
            for mw in self.middleware:
                mw(self.req, self.res)

        handler = getattr(self, self.req.method().lower())
        if not handler:
            return self.res.abort(405)
        return handler(self.req, self.res)

    def validate(self):

        METHOD = self.req.method()

        params = self.params.get(METHOD)
        if not params:
            params = self.params

        if params:
            for param, settings in params.items():
                if settings.get('required') and not self.req.param(param):
                    return False

            for param, value in self.req.params().items():
                settings = params.get(param, None)

                # if there is not props for parameters, check can we receive unrecognized params and allow them further
                if not settings:
                    if self.allow_unrecognized:
                        continue
                    else:
                        return False

                # and now try to convert to needed type
                if settings.get('convert'):
                    try:
                        self.req.param(param, settings.type(value)) # save with new converted type
                    except:
                        return False

                if not self.check_settings(settings, value): return False

        if self.req.is_json:
            return self.validate_json()

        return True

    def check_settings(self, settings, value):
        if not self.validate_func(settings.get('func'), value): return False

        if not self.validate_values(settings.get('values'), value): return False

        if not self.validate_regex(settings.get('regex'), value): return False

        if not self.validate_type(settings.get('type'), value): return False

        max = settings.get('max')
        max = settings.get('min')
        if max:
            if type(value) == str:
                if len(value) > max: return False
            if value > max: return False

        if min:
            if type(value) == str:
                if len(value) < min: return False
            if value < settings.get('min'): return False

        return True

    def validate_func(self, func, value):
        if not func: return True
        if type(func) == str:
            func = getattr(self, func)
        if not func(value):
            return False
        return True

    def validate_values(self, values, value):
        if not values: return True
        if not value in values:
            return False
        return True

    def validate_regex(self, regex, value):
        if not regex: return True
        if not re.match(regex, value):
            return False
        return True

    def validate_type(self, _type, value):
        if not _type: return True
        if not type(value) == _type:
            return False
        return True


    def validate_json(self):

        def has_objects(obj):
            if not type(obj) == dict:
                return False
            for key, value in obj.items():
                 if type(value) == dict:
                     return True
            return False

        def level_params(params, data):

            for param, value in params.items():
                if has_objects(value):
                    if not level_params(value, data.get(param, {})):
                        return False
                else:
                    if value.get('required'):
                        try:
                            data[param]
                        except:
                            return False
            return True

        if not level_params(self.json, self.req.json()):
            return False

        def level(data, params, current_level=0):

            for key, value in data.items():
                current_params = params.get(key)
                if not current_params:
                    if not self.allow_unrecognized:
                        return False
                    else:
                        continue

                if has_objects(value):
                    if not next_params:
                        continue
                    if self.json_maxlevel == current_level + 1:
                        print('json tree level of input data is more than %d. Please, set up View.json_maxlevel to correct integer value' % self.json_maxlevel)
                    if not level(value, next_params, current_level + 1):
                        return False
                else:
                    if not self.check_settings(current_params, value):
                        return False
            return True

        return level(self.req.json(), self.json)
