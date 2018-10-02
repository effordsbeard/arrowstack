import arrow
import os, os.path


class View(arrow.view):

    def get(self, req, res):
        static_path = self.view_params.get('static_path')
        filepath = os.path.join(os.getcwd(), static_path, self.route.get('filename'))

        if not os.path.exists(filepath):
            return res.abort(400)

        if not filepath.startswith(os.path.join(os.getcwd(), static_path)):
            return res.abort(400)
            
        with open(filepath, 'rb') as f:
            res.binary(f.read())
            return res.send()
