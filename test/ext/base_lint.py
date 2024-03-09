import textwrap
from typing import Callable

import pytest
from pytest_common_subject import CommonSubjectTestMixin
from pytest_lambda import lambda_fixture, not_implemented_fixture, static_fixture


class IncludesUnexpectedFocused:
    def it_includes_unexpected_focused_warning(self, focused_warning_text, stdout: str):
        assert focused_warning_text in stdout


class DoesNotIncludeUnexpectedFocused:
    def it_does_not_include_unexpected_focused_warning(self, focused_warning_text, stdout: str):
        assert focused_warning_text not in stdout


class BaseLintTest(CommonSubjectTestMixin):
    #: Test file source code. Overridden by child test contexts
    source = not_implemented_fixture()

    #: Text to be expected in output if focused test is found
    focused_warning_text = not_implemented_fixture()

    @pytest.fixture
    def execute_linter(self, testdir, source_file) -> Callable[[], str]:
        """Run the linter and return the captured stdout"""

        def run_linter_test() -> str:
            result = testdir.run()
            return result.stdout.str()

        return run_linter_test

    @pytest.fixture
    def common_subject(self, execute_linter):
        return execute_linter

    dedented_source = lambda_fixture(lambda source: textwrap.dedent(source))
    source_file = lambda_fixture(lambda dedented_source, testdir: testdir.makepyfile(dedented_source))

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

            class CasePyTestMarkUnpackAssign(IncludesUnexpectedFocused):
                # language=py
                source = lambda_fixture(lambda pytestmark_decl: f'''
                    import pytest

                    class TestMyStuff:
                        pytest._notreal, pytestmark, stuff = 'abc', {pytestmark_decl}, 123

                        def test_stuff(self):
                            pass
                ''')

        class ContextWithoutOnlyMark(DoesNotIncludeUnexpectedFocused):
            # language=py
            source = static_fixture('''
                class TestMyStuff:
                    apples = 'pears'

                    def test_stuff(self):
                        pass
            ''')

    class ContextModule:
        class ContextWithOnlyMark:
            class CaseSingleAssign(IncludesUnexpectedFocused):
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

            class CaseUnpackAssign(IncludesUnexpectedFocused):
                # language=py
                source = lambda_fixture(lambda pytestmark_decl: f'''
                    import pytest

                    pytest._notreal, pytestmark, stuff = 'abc', {pytestmark_decl}, 123

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

    class CaseUnrelated(DoesNotIncludeUnexpectedFocused):
        # language=py
        source = static_fixture('''
            # Ensure proper handling of module-level assignments
            d = dict()
            d['a'] = 1
            d |= {}
            d.keys = lambda x: x

            # Unpacking assignments of all kinds should not cause errors
            a, b, c = 1, 2, 3
            a, *b, c = 1, 2, 3, 4, 5
            a, *b, c = range(3)
            a, b, c = range(3)
            [a, b, c] = range(3)

            # Decorators of all kinds should not cause errors
            @staticmethod
            @a.b.c
            @a.b.c()
            def test_stuff():
                pass
        ''')
