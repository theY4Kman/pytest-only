def pytest_collection_modifyitems(config, items):
    only = [item for item in items if 'only' in item.keywords]
    if only:
        items[:] = only
