import os, os.path


class File(object):

    def __init__(self, cgi_file):
        self.cgi_file = cgi_file
        self.name = cgi_file.filename
        self.binary = cgi_file.value
        self.real_ext = None

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.binary)
