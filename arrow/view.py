from webob import Response
import re


methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

class View(object):

    allow_unrecognized = True
    params = {}
    json = None
    json_maxlevel = 10
    middleware = []

    def __init__(self, req, res, route):
        self.req = req
        self.res = res
        self.route = route

        validation_for_all = True  # if not one of method as key in params
        self.params_settings = self.params

        for key in self.params:
            if key in methods:
                validation_for_all = False
                break

        if validation_for_all:
            for method in methods:
                self.params_settings[method] = self.params  # copy paste of params for each method

    def get(self, req, res):
        return self.res.abort(405)

    def post(self, req, res):
        return self.res.abort(405)

    def put(self, req, res):
        return self.res.abort(405)

    def patch(self, req, res):
        return self.res.abort(405)

    def delete(self, req, res):
        return self.res.abort(405)

    def options(self, req, res):
        return self.res.abort(405)

    def handle(self):
        if not self.validate():
            return self.res.abort(400)

        if self.middleware:
            for mw in self.middleware:
                mw(self.req, self.res)

        if self.req.method() == 'GET':
            self.get(self.req, self.res)
        elif self.req.method() == 'POST':
            self.post(self.req, self.res)
        elif self.req.method() == 'PUT':
            self.put(self.req, self.res)
        elif self.req.method() == 'PATCH':
            self.patch(self.req, self.res)
        elif self.req.method() == 'DELETE':
            self.delete(self.req, self.res)
        elif self.req.method() == 'OPTIONS':
            self.options(self.req, self.res)

    def validate(self):

        METHOD = self.req.method()

        params = self.params_settings.get(METHOD)

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

                if not self.check_settings(settings, value): return False

                # and now try to convert to needed type
                if settings.get('convert'):
                    try:
                        self.req.param(param, settings.type(value)) # save with new converted type
                    except:
                        print('can\'t convert param to type')

        if self.req.is_json:
            return self.validate_json()

        return True

    def check_settings(self, settings, value):
        if not self.validate_func(settings.get('func'), value): return False

        if not self.validate_values(settings.get('values'), value): return False

        if not self.validate_regex(settings.get('regex'), value): return False

        if not self.validate_type(settings.get('type'), value): return False

        return True

    def validate_func(self, func, value):
        if not func: return True
        if not settings['func'](value):
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

        def level(data, params, current_level=0):

            if type(params) == dict:
                for param, settings in params.items():
                    if not has_objects(settings) and settings.get('required') and not data.get(param):
                        return False

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
