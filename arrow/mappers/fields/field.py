class Field(object):

    def __init__(self, data):
        if not isinstance(data, dict):
            data = {
                'type': data
            }
        self.data = data

    def convert(self):
        self.data['convert'] = True
        return self

    def required(self):
        self.data['required'] = True
        return self
