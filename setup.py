import os
from setuptools import setup


PROJECT_DIR = os.path.dirname(__file__)
PKG_DIR = os.path.join(PROJECT_DIR, 'pytest_only')
VERSION_PATH = os.path.join(PKG_DIR, 'version.py')
REQS_PATH = os.path.join(PROJECT_DIR, 'requirements.txt')
README_PATH = os.path.join(PROJECT_DIR, 'README.rst')


def get_version():
    with open(VERSION_PATH) as fp:
        source = fp.read()

    ctx = {}
    exec(source, ctx)
    return ctx['__version__']


def get_requirements():
    with open(REQS_PATH) as fp:
        return list(fp)


def get_readme():
    with open(README_PATH) as f:
        return f.read()


setup(
    name='pytest-only',
    url='https://github.com/theY4Kman/pytest-only',
    version=get_version(),
    description='Use @pytest.mark.only to run a single test',
    long_description=get_readme(),
    author='Zach "theY4Kman" Kanzler',
    author_email='they4kman@gmail.com',
    packages=['pytest_only'],
    entry_points={
        'pytest11': [
            'only = pytest_only.plugin',
        ]
    },
    classifiers=[
        'Framework :: Pytest',
    ],
    install_requires=get_requirements(),
    include_package_data=True,
)
