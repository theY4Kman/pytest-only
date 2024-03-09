from typing import Callable

import pytest
from pytest_lambda import static_fixture

from .base_lint import BaseLintTest


class DescribePylint(BaseLintTest):
    focused_warning_text = static_fixture('unexpected-focused')

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
    def execute_linter(self, testdir, pylint_rc, source_file) -> Callable[[], str]:
        """Run the linter and return the captured stdout"""

        def run_linter_test() -> str:
            result = testdir.runpytest(
                # Run only the generated pylint "tests"
                '--pylint',

                # And don't load pytest-only, or it will deselect the pylint tests!
                '-p', 'no:only',

                # Explicitly define the pylint config file to use
                '--pylint-rcfile', pylint_rc.strpath,
            )
            return result.stdout.str()

        return run_linter_test
