from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


major = 0
minor = 1
patch = 0
version = '.'.join([str(v) for v in [major, minor, patch]])


setup(name='spomato',
      version=version,
      description='Tomato Timer with Spotify',
      url='https://github.com/pm8k/spomato',
      download_url = 'https://github.com/pm8k/spomato/archive/0.1.tar.gz', # I'll explain this in a second

      long_description=readme(),
      author='Matthew Russell',
      author_email='astromars42@gmail.com',
      license='MIT',
      keywords=['python', 'spotify', 'spotipy', 'tomato', 'timer', 'music'],

      packages=['spomato'],
        install_requires=[
          'spotipy',
          'splinter',
          'pandas'
      ],
      include_package_data=True,

      zip_safe=False)
