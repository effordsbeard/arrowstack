class Object(object):

    def __init__(self, data={}, recursive=True):
        self.recursive = recursive
        for key, value in data.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        if type(value) == dict and self.recursive:
            value = Object(dict)
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__.get(name, None)
