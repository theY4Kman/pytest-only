def pytest_addoption(parser):
    parser.addoption('--only', dest='enable_only',
                     default=True, action='store_true',
                     help='Only run tests with the "only" marker')

    parser.addoption('--no-only', dest='enable_only',
                     action='store_false',
                     help='Disable --only filtering')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--only'):
        return

    only, other = [], []
    for item in items:
        l = only if item.get_marker('only') else other
        l.append(item)

    if only:
        items[:] = only
        if other:
            config.hook.pytest_deselected(items=other)
