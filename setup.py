# To use a consistent encoding
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
  name='romanizer',
  packages=find_packages(),
  install_requires=['requests', 'pyonmttok', 'python-Levenshtein'],
  data_files=[('romanizer', ['romanizer/dakshina_lexicon.json'])]
)
