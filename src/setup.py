__author__="snbuback"
__date__ ="$Nov 20, 2009 6:45:20 PM$"

from setuptools import setup,find_packages

setup (
  name = 'XenAutoMigrate',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'snbuback',
  author_email = '',

  summary = 'Just another Python package for the cheese shop',
  url = '',
  license = '',
  long_description= 'Long description of the package',

  # could also include long_description, download_url, classifiers, etc.

  
)