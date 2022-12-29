from setuptools import setup, find_packages
from checkuser import __version__, __author__, __email__

PACKAGES = find_packages()
REQUIREMENTS = ['flask', 'flask-sock', 'flask-socketio', 'eventlet']
VERSION = __version__

DESCRIPTION = open('README.md').read()
AUTHOR = __author__
AUTHOR_EMAIL = __email__
URL = 'https://github.com/DTunnel0/DTCheckUser'
LICENSE = 'MIT'

setup(
    name='CheckUser',
    version=VERSION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'checkuser = checkuser.__main__:main',
        ],
    },
)
