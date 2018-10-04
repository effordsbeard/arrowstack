import arrow
import os, os.path


class View(arrow.view):

    def get(self, req, res):
        static_path = os.path.join(os.getcwd(), self.view_params.get('static_path'))
        exclude = self.view_params.get('exclude')
        filepath = os.path.join(static_path, self.route.get('filename'))
        for exclude_path in exclude:
            if filepath.startswith(exclude_path):
                return res.abort(400)

        if not os.path.exists(filepath):
            return res.abort(404)

        if not filepath.startswith(static_path):
            return res.abort(400)

        res.header('Content-Type', arrow.mime.get(os.path.splitext(filepath)[1], ''))

        with open(filepath, 'rb') as f:
            res.binary(f.read())
            return res.send()
