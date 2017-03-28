def pytest_collection_modifyitems(config, items):
    only, other = [], []
    for item in items:
        l = only if item.get_marker('only') else other
        l.append(item)

    if only:
        items[:] = only
        if other:
            config.hook.pytest_deselected(items=other)
