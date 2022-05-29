import pytest


@pytest.fixture(autouse=True)
def pylint_rc(testdir):
    return testdir.makefile('.rc', pylint='''
        [MASTER]
        load-plugins=pytest_only.ext.pylint
    
        [MESSAGES CONTROL]
        enable=unexpected-focused
    ''')


@pytest.fixture
def run_pylint_test(testdir, pylint_rc):
    def run_pylint_test(source: str) -> str:
        testdir.makepyfile(source)
        result = testdir.runpytest(
            # Run only the generated pylint "tests"
            '--pylint',

            # And don't load pytest-only, or it will deselect the pylint tests!
            '-p', 'no:only',

            # Explicitly define the pylint config file to use
            '--pylint-rcfile', pylint_rc.strpath,
        )
        return result.stdout.str()
    return run_pylint_test


def test_unexpected_focused_with_decorator(run_pylint_test):
    result = run_pylint_test(
        'import pytest\n'
        '\n'
        '@pytest.mark.only\n'
        'def test_stuff():\n'
        '    pass\n'
    )
    assert 'unexpected-focused' in result


def test_no_unexpected_focused_without_decorator(run_pylint_test):
    result = run_pylint_test(
        'def test_stuff():\n'
        '    pass\n'
    )
    assert 'unexpected-focused' not in result
