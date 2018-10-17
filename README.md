# Arrow Framework

## Installation

```shell
pip install https://github.com/effordsbeard/arrowstack/archive/master.zip
```

## Basic usage

```python=
import arrow

class View(arrow.view):

    def get(self):
        res.send('arrow')

arrow.route('/', view=View, name="index")
arrow.run()  # uses gunicorn from the box
```

## Declarative validation

```python=
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
            'ext': '.png'  # extension is validated by real mime type from binary data
        }
    }

    def get(self, req, res): # you can pass req and res params to method or get them via self.req and self.res
        res.cookie('newcookie', req.param('test'))

    def post(self):
        file = self.req.file('file1')
        file.save('/path/to/file%s' % file.real_ext )
        self.res.ok()
```

## Auto importing views

### Structure
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
```python=
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
```python=
    import arrow

    class View(arrow.view):  # class name must be View for auto importinh
        def get(self):
            return arrow.render('index.tpl', data={'message': 'hello, world'})  # uses tequilla template engine
```

views/users/index.py
```python=
import arrow
...
...
```

templates/index.tpl
```htmlmixed=
<html>
    <head></head>
    <body>
        {{data['message']}}
    </body>
</html>
```

Don't forget change working directory to **app**
```shell=
cd app
python run.py
```


## WSGI app

```python=
wsgi = arrow.wsgi_handler
```

```shell=
cd app
gunicorn run:wsgi
```
