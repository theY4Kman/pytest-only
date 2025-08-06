from importlib import metadata

try:
    __version__ = metadata.version('pytest-only')
except metadata.PackageNotFoundError:
    __version__ = 'dev'
