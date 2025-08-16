import os

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
    entry_points = {
        'console_scripts': [
            'multitool=multitool.__main__:main'
        ]
    },
    install_requires = [
        'click>=8.1.3',
        'click-aliases>=1.0.1',
        'click-option-group>=0.5.5',
        'gitpython>=3.1.30'
    ],
    python_requires=">=3.7",
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
