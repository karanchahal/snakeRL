from os.path import join, dirname, realpath
from setuptools import setup
import sys

assert sys.version_info.major == 3 and sys.version_info.minor >= 6, \
    "The Snake RL repo is designed to work with Python 3.6 and greater." \
    + "Please install it before proceeding."

with open(join("snakeRL", "version.py")) as version_file:
    exec(version_file.read())

setup(
    name='snakeRL',
    py_modules=['snakeRL'],
    version=__version__,#'0.0.1',
    install_requires=[
        'gym[atari,box2d,classic_control]>=0.10.8',
        'pygame',
        'numpy'
    ],
    description="Snake Game Multi Agent Setting with Deep RL",
    author="Karanbir Chahal",
)