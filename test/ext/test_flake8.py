import ast
from typing import Callable

import pytest
from pytest_lambda import static_fixture

from pytest_only.ext.flake8 import PytestOnlyMarkVisitor
from .base_lint import BaseLintTest


class DescribeFlake8Plugin(BaseLintTest):
    focused_warning_text = static_fixture('PTO01')

    @pytest.fixture
    def execute_linter(self, testdir, source_file) -> Callable[[], str]:
        """Run the linter and return the captured stdout"""

        def run_linter_test() -> str:
            result = testdir.run('flake8', '.')
            return result.stdout.str()

        return run_linter_test


class DescribePytestOnlyMarkVisitor(BaseLintTest):
    focused_warning_text = static_fixture('PTO01')

    @pytest.fixture
    def execute_linter(self, dedented_source) -> Callable[[], str]:
        """Run the linter and return the captured stdout"""

        def run_linter_test() -> str:
            tree = ast.parse(dedented_source)
            visitor = PytestOnlyMarkVisitor()
            visitor.visit(tree)
            return '\n'.join(
                f'{lineno}:{col_offset} {msg}'
                for lineno, col_offset, msg in visitor.errors
            )

        return run_linter_test
