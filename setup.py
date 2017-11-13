"""Setup file for pygame-assets.

NOTES: registering a package on PyPI

1. Register and upload on PyPI's test servers
python setup.py register -r pypitest
python setup.py sdist upload -r pypitest

2. If everything went fine, you can go live!
python setup.py register -r pypi
python setup.py sdist upload -r pypi
"""

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


def read(fname):
    """Return content of a file."""
    with open(path.join(here, fname)) as f:
        return f.read()


NAME = 'pygame_assets'
VERSION = '0.1'
DESCRIPTION = 'Assets manager for Pygame apps'
LONG_DESCRIPTION = read('README.md')

URL = 'https://github.com/florimondmanca/pygame-assets'
DOWNLOAD_URL = URL + '/archive/{tag}.tar.gz'.format(tag=VERSION)

AUTHOR = 'Florimond Manca'
AUTHOR_EMAIL = 'florimond.manca@gmail.com'

KEYWORDS = 'pygame asset management game utility'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Libraries :: pygame',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    download_url=DOWNLOAD_URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=('example_project',)),
    python_requires='>=3.4',
    include_package_data=True,
)
