class Object(object):

    def __init__(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        if type(value) == dict:
            value = Object(dict)
        self.__dict__[name] = value
