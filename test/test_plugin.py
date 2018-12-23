import os

import pytest


pytest_plugins = 'pytester'


@pytest.fixture(autouse=True)
def setup_syspath(testdir):
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    testdir.syspathinsert(repo_dir)
    testdir.makeconftest('pytest_plugins = "pytest_only.plugin"')


def assert_test_did_run(res, name):
    res.stdout.fnmatch_lines('*' + name + '*')


def assert_test_did_not_run(res, name):
    with pytest.raises(pytest.fail.Exception):
        res.stdout.fnmatch_lines('*' + name + '*')


def test_function(testdir):
    file = testdir.makepyfile('''
        import pytest

        def test_should_not_run():
            pass

        @pytest.mark.only
        def test_should_run():
            pass

        def test_should_also_not_run():
            pass
    ''')
    res = testdir.runpytest_inprocess(file, '--verbose')
    outcomes = res.parseoutcomes()
    assert 'passed' in outcomes, 'Tests did not run successfully'
    assert outcomes['passed'] == 1, 'Incorrect number of tests passed'

    assert_test_did_run(res, 'test_should_run')
    assert_test_did_not_run(res, 'test_should_not_run')
    assert_test_did_not_run(res, 'test_should_also_not_run')


def test_class(testdir):
    file = testdir.makepyfile('''
        import pytest

        def test_should_not_run():
            pass

        @pytest.mark.only
        class TestShouldRun:
            def test_should_run(self):
                pass

            def test_should_also_run(self):
                pass

        class TestShouldNotRun:
            def test_should_also_not_run(self):
                pass
    ''')
    res = testdir.runpytest_inprocess(file, '--verbose')
    outcomes = res.parseoutcomes()
    assert 'passed' in outcomes, 'Tests did not run successfully'
    assert outcomes['passed'] == 2, 'Incorrect number of tests passed'

    assert_test_did_run(res, 'test_should_run')
    assert_test_did_run(res, 'test_should_also_run')
    assert_test_did_not_run(res, 'test_should_not_run')
    assert_test_did_not_run(res, 'test_should_also_not_run')


def test_file(testdir):
    should_run = testdir.makepyfile(should_run='''
        import pytest

        pytestmark = pytest.mark.only

        def test_should_run():
            pass

        def test_should_also_run():
            pass
    ''')

    should_not_run = testdir.makepyfile(should_not_run='''
        def test_should_not_run():
            pass
    ''')

    res = testdir.runpytest_inprocess('--verbose', should_run, should_not_run)
    outcomes = res.parseoutcomes()
    assert 'passed' in outcomes, 'Tests did not run successfully'
    assert outcomes['passed'] == 2, 'Incorrect number of tests passed'

    assert_test_did_run(res, 'test_should_run')
    assert_test_did_run(res, 'test_should_also_run')
    assert_test_did_not_run(res, 'test_should_not_run')


def test_no_only_cmdline_option(testdir):
    file = testdir.makepyfile('''
        import pytest

        def test_should_run_as_well():
            pass

        @pytest.mark.only
        def test_should_run():
            pass

        def test_should_also_run():
            pass
    ''')
    res = testdir.runpytest_inprocess(file, '--verbose', '--no-only')
    outcomes = res.parseoutcomes()
    assert 'passed' in outcomes, 'Tests did not run successfully'

    assert_test_did_run(res, 'test_should_run')
    assert_test_did_run(res, 'test_should_run_as_well')
    assert_test_did_run(res, 'test_should_also_run')


def test_negating_cmdline_options(testdir):
    file = testdir.makepyfile('''
        import pytest

        def test_should_not_run():
            pass

        @pytest.mark.only
        def test_should_run():
            pass

        def test_should_also_not_run():
            pass
    ''')
    res = testdir.runpytest_inprocess(file, '--verbose', '--no-only', '--only')
    outcomes = res.parseoutcomes()
    assert 'passed' in outcomes, 'Tests did not run successfully'

    assert_test_did_run(res, 'test_should_run')
    assert_test_did_not_run(res, 'test_should_also_not_run')
    assert_test_did_not_run(res, 'test_should_not_run')
