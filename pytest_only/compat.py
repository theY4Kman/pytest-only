import pytest

try:
    from _pytest.nodes import Node
except ImportError:
    from _pytest.main import Node


if hasattr(Node, 'get_closest_marker'):
    get_closest_marker = lambda item, *a, **kw: item.get_closest_marker(*a, **kw)
elif hasattr(Node, 'get_marker'):
    get_closest_marker = lambda item, *a, **kw: item.get_marker(*a, **kw)
else:
    raise RuntimeError(
        'Unable to determine get_closest_marker alternative '
        'for pytest version {}'.format(pytest.__version__))
