def pytest_addoption(parser):
    parser.addoption('--only', dest='enable_only',
                     default=True, action='store_true',
                     help='Only run tests with the "only" marker')

    parser.addoption('--no-only', dest='enable_only',
                     action='store_false',
                     help='Disable --only filtering')


def get_closest_marker(item):
    # get_closest_marker added in ptest 3.6
    # https://docs.pytest.org/en/latest/changelog.html#pytest-3-6-0-2018-05-23
    # get_marker removed in pytest 4.1
    # https://docs.pytest.org/en/latest/changelog.html#pytest-4-1-0-2019-01-05
    if hasattr(item, 'get_closest_marker'):
        fn = 'get_closest_marker'
    else:
        fn = 'get_marker'
    return getattr(item, fn)('only')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--only'):
        return

    only, other = [], []
    for item in items:
        l = only if get_closest_marker(item) else other
        l.append(item)

    if only:
        items[:] = only
        if other:
            config.hook.pytest_deselected(items=other)
