from setuptools import setup
from staticrss import __version__


setup(name='staticrss',
      version=__version__,
      author='Matthias Vogelgesang',
      author_email='matthias.vogelgesang@gmail.com',
      license='MIT',
      url='https://github.com/matze/staticrss',
      description='Static site generator for RSS and Atom feeds',
      long_description=open('README.rst').read(),
      packages=['staticrss'],
      scripts=['bin/srss'],
      install_requires=['python-dateutil',
                        'pytz',
                        'feedcache',
                        'feedparser',
                        'jinja2',
                        'PyYAML'],
      test_suite='tests')
