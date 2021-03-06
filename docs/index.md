# Introduction

Arrow is for writing expressive and declarative code. Arrow decrease lines of code without untraced magic. It uses tested and proved by time libraries for handling requests (webob, routes, cgi). Arrow targets on writing less with ready to start application in minutes.

There is several features from the box provided as middleware and simple functionality for writing your own.

# Installation

```shell
pip install https://github.com/effordsbeard/arrowstack/archive/master.zip
```

# Basic usage

```python
import arrow

class View(arrow.view):

    def get(self):
        res.send('arrow')

arrow.route('/', view=View, name="index")
arrow.run()  # uses gunicorn from the box
```

# Validation

```python
class View(arrow.view):

    params = {
        'GET': {
            'test': {
                'regex': r'\d{5,}',
                'required': True,
                'convert': True,  # make type conversion if type validation is on
                'type': int  # or you can just check param can be converted
            }
        },
    }

    files = {
        'file1': {
            'max': 1000000000,  # KB if you don't use WAF or web server limits
            'ext': '.png'  # extension is validated by real mime type from binary data,
            'required': True  # one line here and no if's and http aborting
        }
    }

    def get(self, req, res): # you can pass req and res params to method or get them via self.req and self.res
        res.cookie('newcookie', req.param('test'))
        req.header('Location', 'http://google.com')
        res.status(301)
        # or res.redirect()
        res.send()  # here is the end of http handling

        #...some code after response to client
        return  # here is the end signal for worker process and res.send() if if was not called before

    def post(self):
        file = self.req.file('file1')
        file.save('/path/to/file%s' % file.real_ext )
        self.res.ok()
```

# Auto importing views

Structure
```
app
|    templates
|        index.tpl
|    views
|        users
|            index.py
|        index.py
|    run.py
```
run.py
```python
    import arrow
    import os

    arrow.templates('templates')
    arrow.route('/', 'views.index')
    arrow.route('/users', 'views.users.index')
    arrow.run({
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT')
    })
```

views/index.py
```python
    import arrow

    class View(arrow.view):  # class name must be View for auto importinh
        def get(self):
            return arrow.render('index.tpl', data={'message': 'hello, world'})  # uses tequilla template engine
```

views/users/index.py
```python
import arrow
...
...
```

templates/index.tpl
```html
<html>
    <head></head>
    <body>
        {{data['message']}}
    </body>
</html>
```

Don't forget change working directory to **app**
```shell
cd app
python run.py
```

## Proxy

```python
import arrow

arrow.route('/', 'views.index')
arrow.route('/auth', 'views.auth.index')
```

views/index.py
```python
import arrow

class View(arrow.view):

  def get(self):
    res = arrow.proxy(self.req, 'views.auth.index')
    res.send()
```


## WSGI app

```python
import arrow
wsgi = arrow.wsgi_handler
```

```shell
cd app
gunicorn run:wsgi
```
