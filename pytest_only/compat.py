import pytest

try:
    from _pytest.nodes import Node
except ImportError:
    from _pytest.main import Node


if hasattr(Node, 'get_closest_marker'):
    def get_closest_marker(item: Node, *args, **kwargs):
        return item.get_closest_marker(*args, **kwargs)
elif hasattr(Node, 'get_marker'):
    def get_closest_marker(item: Node, *args, **kwargs):
        return item.get_marker(*args, **kwargs)
else:
    raise RuntimeError(
        'Unable to determine get_closest_marker alternative '
        'for pytest version {}'.format(pytest.__version__)
    )
