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
      url='http://github.com/pm8k/spomato',
      long_description=readme(),
      author='PM8K',
      author_email='astromars42@gmail.com',
      license='MIT',
      packages=['spomato'],
        install_requires=[
          'spotipy',
          'splinter',
          'pandas'
      ],
      include_package_data=True,

      zip_safe=False)
