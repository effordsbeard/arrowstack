import base64


class HttpAuth(object):

    def __init__(self, username=None, password=None, users=None, auth_func=None):
        if not users:
            users = {}
            users[username] = password
        self.users = users
        self.auth_func = auth_func

    def __call__(self, req, res):
        auth_header = req.header('Authorization')

        if not auth_header:
            res.status(401)
            res.header('WWW-Authenticate', 'Basic realm="Provide credentials", charset="UTF-8"')
            return res.send()

        token = None
        try:
            authtype, token = auth_header.split(' ')
            if not authtype == 'Basic':
                return res.abort(403)
        except:
            return res.abort(400)

        username, password = base64.b64decode(token).decode("utf-8").split(':')

        if self.check_user(username, password):
            return res.ok()
        else:
            res.status(401)
            res.header('WWW-Authenticate', 'Basic realm="Provide credentials", charset="UTF-8"')
            return res.send()

    def check_user(self, username, password):
        for _username, _password in self.users.items():
            if username == _username and password == _password:
                return True
        if self.auth_func:
            if self.auth_func(username, password):
                return True

        return False
