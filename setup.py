import os, sys, re

from multitool import APP
from multitool import __version__ as version
from multitool import description

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()

SETUP_ARGS = dict(
    name=APP,
    version=version,
    description=(description),
    long_description=long_description,
    url='https://github.com/mdelotavo/multitool',
    author='Matthew Delotavo',
    author_email='matthew.t.delotavo@gmail.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    # py_modules = ['multitool',],
    entry_points='''
        [console_scripts]
        multitool=multitool.__main__:cli
    ''',
    install_requires = [
        'requests>=2.22',
        'click',
        'click-aliases',
        'click-option-group',
        'colorama',
        'pyotp',
        'requests',
        'tqdm',
        'tabulate',
        'pyjwt',
        'python-gnupg>=0.3.5',
        'gitpython'
    ],
    python_requires=">=3.6",
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
