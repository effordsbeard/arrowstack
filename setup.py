from setuptools import setup, find_packages

setup(
    name='ArrowStack',
    version='0.1dev',
    packages=['arrow', 'arrowstack', 'arrow.middleware'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'arrowstack = arrowstack:main'
        ]
    },
    install_requires=[
        'routes',
        'webob',
        'docker',
        'pymist',
        'gunicorn'
    ]
)
