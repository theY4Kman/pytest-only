import textwrap

import pytest
from pytest_common_subject import CommonSubjectTestMixin
from pytest_lambda import lambda_fixture, not_implemented_fixture, static_fixture


class IncludesUnexpectedFocused:
    def it_includes_unexpected_focused_warning(self, stdout: str):
        assert 'unexpected-focused' in stdout


class DoesNotIncludeUnexpectedFocused:
    def it_does_not_include_unexpected_focused_warning(self, stdout: str):
        assert 'unexpected-focused' not in stdout


class DescribePylint(CommonSubjectTestMixin):
    #: Test file source code. Overridden by child test contexts
    source = not_implemented_fixture()

    @pytest.fixture(autouse=True)
    def pylint_rc(self, testdir):
        return testdir.makefile(
            ext='.rc',
            pylint='''
                [MASTER]
                load-plugins=pytest_only.ext.pylint

                [MESSAGES CONTROL]
                enable=unexpected-focused
            '''
        )

    @pytest.fixture
    def common_subject(self, testdir, pylint_rc, source):
        def run_pylint_test() -> str:
            testdir.makepyfile(textwrap.dedent(source))
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

    # Domain-specific alias
    stdout = lambda_fixture('common_subject_rval')

    # Used to verify pytestmark behaviour
    pytestmark_decl = lambda_fixture(params=[
        pytest.param('pytest.mark.only', id='single'),
        pytest.param('[pytest.mark.only]', id='list'),
        pytest.param('[pytest.mark.other, pytest.mark.only, pytest.mark.stuff]', id='list-multi'),
    ])

    class ContextFunction:
        class ContextWithOnlyMark(IncludesUnexpectedFocused):
            # language=py
            source = static_fixture('''
                import pytest

                @pytest.mark.only
                def test_stuff():
                    pass
            ''')

        class ContextWithoutOnlyMark(DoesNotIncludeUnexpectedFocused):
            # language=py
            source = static_fixture('''
                def test_stuff():
                    pass
            ''')

    class ContextAsyncFunction:
        class ContextWithOnlyMark(IncludesUnexpectedFocused):
            # language=py
            source = static_fixture('''
                import pytest

                @pytest.mark.asyncio
                @pytest.mark.only
                async def test_stuff():
                    pass
            ''')

        class ContextWithoutOnlyMark(DoesNotIncludeUnexpectedFocused):
            # language=py
            source = static_fixture('''
                import pytest

                @pytest.mark.asyncio
                async def test_stuff():
                    pass
            ''')

    class ContextClass:
        class ContextWithOnlyMark:
            class CaseDecorator(IncludesUnexpectedFocused):
                # language=py
                source = static_fixture('''
                    import pytest

                    @pytest.mark.only
                    class TestMyStuff:
                        def test_stuff(self):
                            pass
                ''')

            class CasePyTestMark(IncludesUnexpectedFocused):
                # language=py
                source = lambda_fixture(lambda pytestmark_decl: f'''
                    import pytest

                    class TestMyStuff:
                        pytestmark = {pytestmark_decl}

                        def test_stuff(self):
                            pass
                ''')

        class ContextWithoutOnlyMark(DoesNotIncludeUnexpectedFocused):
            # language=py
            source = static_fixture('''
                class TestMyStuff:
                    def test_stuff(self):
                        pass
            ''')

    class ContextModule:
        class ContextWithOnlyMark(IncludesUnexpectedFocused):
            # language=py
            source = lambda_fixture(lambda pytestmark_decl: f'''
                import pytest

                pytestmark = {pytestmark_decl}

                class TestMyStuff:
                    def test_stuff(self):
                        pass

                def test_other_stuff():
                    pass
            ''')

        class ContextWithoutOnlyMark(DoesNotIncludeUnexpectedFocused):
            # language=py
            source = static_fixture('''
                class TestMyStuff:
                    def test_stuff(self):
                        pass
            ''')
