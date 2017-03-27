import os
from setuptools import setup


project_dir = os.path.dirname(__file__)


def requirements():
    reqs_path = os.path.join(project_dir, 'requirements.txt')
    with open(reqs_path) as fp:
        return list(fp)


def readme():
    readme_path = os.path.join(project_dir, 'README.rst')
    with open(readme_path) as f:
        return f.read()

setup(
    name='pytest-only',
    url='https://github.com/theY4Kman/pytest-only',
    version='1.0.0',
    description='Use @pytest.mark.only to run a single test',
    long_description=readme(),
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
    install_requires=requirements(),
    include_package_data=True,
)
