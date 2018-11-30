import json
import re
from .fields.field import Field


class Mapper(object):

    def __init__(self, data):
        if not data:
            data = {}

        self.__data = data

        if hasattr(self, 'set'):
            self.set(data)


    def valid(self, _settings=None, data=None):
        props = self.props()
        # print(props)
        if _settings:
            props = _settings.items()
        if not data:
            data = self.__data
        for prop, settings in props:
            print(prop, settings)
            if not self.validate_value(settings, data.get(prop)):
                return False
            # if not self.__no_dicts__(settings):
            #     for sub_key, sub_value in settings:
            #         if not self.valid(settings.get(sub_key), sub_value):
            #             return False
            #     if not self.valid(settings, data.get(prop, {})):
            #         return False
            # else:
            #     if data.get(prop) and not self.validate_value(settings, data.get(prop)):
            #         return False

        return True

    def validate_value(self, settings, value):
        if isinstance(settings, list):
            if not len(list):
                settings = {
                    ''
                }
        if settings.get('required'):
            if not value:
                return False

        if settings.get('convert'):
            try:
                self.req.param(param, settings.type(value)) # save with new converted type
            except:
                return False

        _type = settings.get('type')
        if _type:
            if not type(value) == _type:
                return False
            return True

        func = settings.get('func')
        if func:
            if type(func) == str:
                func = getattr(self, func)
            if not func(value):
                return False
            return True

        values = settings.get('values')
        if values:
            if not value in values:
                return False
            return True

        regex = settings.get('regex')
        if regex:
            if not re.match(regex, value):
                return False
            return True

        _max = settings.get('max')
        _min = settings.get('min')

        if _max:
            if type(value) == str:
                if len(value) > _max: return False
            if value > _max: return False

        if _min:
            if type(value) == str:
                if len(value) < _min: return False
            if value < _min: return False

            return True

    def __no_dicts__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                return False
        return True

    def props(self):
        res = [(attr, getattr(self, attr).data) for attr in dir(self)
              if isinstance(getattr(self, attr), Field)]
        return res

    # def __getattr__(self, name):
    #     return self.__dict__.get(name)

    def __nonzero__(self):
        return self.valid()

    def __eq__(self, other):
        for prop, value in self.props():
            if not value == getattr(other, prop):
                return False
        return True

    def __contains__(self, prop):
        if self.__dict__.get(prop):
            return True
        return False

    def __repr__(self):
        res = {

        }
        for key, value in self.__dict__.items():
            res[key] = repr(value)
        return json.dumps(res).encode('utf-8').decode('unicode_escape')
