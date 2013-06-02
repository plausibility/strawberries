from setuptools import setup
import strawberries


def long_desc():
    with open('README.rst', 'rb') as f:
        return f.read()

kw = {
    "name": "strawberries",
    "version": strawberries.__version__,
    "description": 'Strawberries is an IRC bot, and also the plural of the word "strawberry".',
    "long_description": long_desc(),
    "url": "https://github.com/plausibility/strawberries",
    "author": "plausibility",
    "author_email": "chris@gibsonsec.org",
    "license": "MIT",
    "packages": [
        'strawberries'
    ],
    "install_requires": [
        "girclib==0.1-dev"
    ],
    "dependency_links": [
        "https://github.com/plausibility/gIRClib/zipball/master#egg=girclib-0.1-dev",
    ],
    "zip_safe": False,
    "keywords": "irc bot strawberries jam",
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Communications :: Chat :: Internet Relay Chat"
    ]
}

if __name__ == "__main__":
    setup(**kw)
