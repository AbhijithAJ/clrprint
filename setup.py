# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
"""Setup for the clrprint package."""

#from distutils.core import setup
from setuptools import setup, Extension

with open('README.md','r') as f:
    README = f.read()

setup(
    author="ABHIJITH BOPPE",
    author_email="abhijithas.eh@gmail.com",
    name='clrprint',
    license="MIT",
    description='''Print colorfull output in IDLE, powershell, and terminal. Supports on DEBUG feature and 
    returns None if user input is not entered in given time. ''',
    version='v2.0.1',
    long_description_content_type='text/markdown',
    long_description=README,
    keywords=['basic colors', 'color print', 'cmd', 'color idle', 'color terminal',
              'color powershell', 'color idle and terminal', 'color idle, cmd, powershell', 'input timeout', 'non blocking input',
               'X-platform', 'DEBUG', 'timed input', 'Cross-platform'],
    url='https://github.com/AbhijithAJ/clrprint',
    download_url='https://github.com/AbhijithAJ/clrprint/archive/refs/tags/v2.0.1.tar.gz',
    packages=['clrprint'],
    python_requires=">=3.2",
    install_requires=['termcolor', 'colorama'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
