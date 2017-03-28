def pytest_collection_modifyitems(config, items):
    only = [item for item in items if item.get_marker('only')]
    if only:
        items[:] = only
