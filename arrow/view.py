from webob import Response


class View(object):

    def get(self, req, res):
        res.status(501)

    def post(self, req, res):
        res.status(501)

    def put(self, req, res):
        res.status(501)

    def patch(self, req, res):
        res.status(501)

    def delete(self, req, res):
        res.status(501)

    def options(self, req, res):
        if self.crossorigin:
            res.header('Access-Control-Allow-Origin', '*')

    def handle(self, req, res):
        if self.middleware:
            for mw in self.middleware:
                mw(req, res)

        if req.method() == 'GET':
            self.get(req, res)
        elif req.method() == 'POST':
            self.post(req, res)
        elif req.method() == 'PUT':
            self.put(req, res)
        elif req.method() == 'PATCH':
            self.patch(req, res)
        elif req.method() == 'DELETE':
            self.delete(req, res)
        elif req.method() == 'OPTIONS':
            self.options(req, res)
