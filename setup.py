"""Author: Matthew Russell

Setup file for Spomato

"""

from setuptools import setup, find_packages

def readme():
    """Opens the readme file and returns it as a string

    Returns
    -------
    string:
        A string representation of the readme file

    """
    with open('README.md') as file:
        return file.read()


MAJOR = 0
MINOR = 2
PATCH = 0
VERSION = '.'.join([str(v) for v in [MAJOR, MINOR, PATCH]])


setup(name='spomato',
      version=VERSION,
      description='Tomato Timer with Spotify',
      url='https://github.com/pm8k/spomato',
      download_url='https://github.com/pm8k/spomato/archive/{V}.tar.gz'.format(V=VERSION),
      long_description=readme(),
      author='Matthew Russell',
      author_email='astromars42@gmail.com',
      license='MIT',
      keywords=['python', 'spotify', 'spotipy', 'tomato', 'timer', 'music'],
      py_modules=['spomato'],
      packages=['spomato'],
      install_requires=[
          'pandas',
          'spotipy'
          ],
      include_package_data=True,

      zip_safe=False)
