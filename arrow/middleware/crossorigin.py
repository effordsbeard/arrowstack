class Crossorigin(object):

    def __init__(self, origin="*", methods=None, max_age=21600, headers=None):
        self.origin = origin
        self.methods = methods
        self.max_age = max_age
        if headers:
            self.headers = ', '.join(headers)
        else:
            self.headers = '*'

    def getmethods(self):
        if self.methods is not None:
            return ', '.join(sorted(x.upper() for x in self.methods))
        else:
            return ''

    def getheaders(self):
        if self.headers is not None:
            return ', '.join(sorted(x.upper() for x in self.headers))
        else:
            return ''

    def __call__(self, req, res):
        res.header('Access-Control-Allow-Origin', self.origin)
        res.header('Access-Control-Allow-Methods', self.getmethods())
        res.header('Access-Control-Max-Age', str(self.max_age))
        res.header('Access-Control-Allow-Headers', self.headers)
        if req.method() == 'OPTIONS':
            res.ok()
            return False
