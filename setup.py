"""Setup file for pygame-assets.

NOTES: registering a package on PyPI

1. Register and upload on PyPI's test servers
python setup.py register -r pypitest
python setup.py sdist upload -r pypitest

2. If everything went fine, you can go live!
python setup.py register -r pypi
python setup.py sdist upload -r pypi
"""

from distutils.core import setup

PACKAGE_NAME = 'pygame_assets'
PACKAGES = [PACKAGE_NAME]
DESCRIPTION = 'Assets manager for Pygame apps'
KEYWORDS = ['pygame', 'assets', 'manager', 'utility']
VERSION = '0.1'

AUTHOR = 'Florimond Manca'
EMAIL = 'florimond.manca@gmail.com'

GITHUB_URL = 'https://github.com/florimondmanca/pygame-assets'
DOWNLOAD_URL = GITHUB_URL + '/archive/{tag}.tar.gz'.format(tag=VERSION)

CLASSIFIERS = [
    'Topic :: Software Development :: Libraries :: pygame',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

setup(
    name=PACKAGE_NAME,
    packages=PACKAGES,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    download_url=DOWNLOAD_URL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
)
