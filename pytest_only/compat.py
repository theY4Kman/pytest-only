import pytest
from _pytest.nodes import Node


if hasattr(Node, 'get_closest_marker'):
    get_closest_marker = Node.get_closest_marker
elif hasattr(Node, 'get_marker'):
    get_closest_marker = Node.get_marker
else:
    raise RuntimeError(
        'Unable to determine get_closest_marker alternative '
        'for pytest version {}'.format(pytest.__version__))
