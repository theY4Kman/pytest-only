from __future__ import annotations

import ast
from typing import Iterable, Tuple, List, Union, Optional


class PytestOnlyMarkChecker:
    """Check for stray pytest.mark.only decorators"""

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def run(self) -> Iterable[Tuple[int, int, str, PytestOnlyMarkVisitor]]:
        visitor = PytestOnlyMarkVisitor()
        visitor.visit(self.tree)
        for lineno, col_offset, msg in visitor.errors:
            yield lineno, col_offset, msg, self


class PytestOnlyMarkVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def add_error(self, node: ast.AST, code: str, msg: str):
        self.errors.append((node.lineno, node.col_offset, f'{code}: {msg}'))

    def add_focused_error(self, node: ast.AST, node_type: str, name: str):
        self.add_error(node, 'PTO01', f'Unexpected focused test using pytest.mark.only: {node_type} {name}')

    def visit_FunctionDef(self, node: ast.FunctionDef):
        funcdef = node

        if not funcdef.decorator_list:
            return

        func_type = 'async def' if isinstance(funcdef, ast.AsyncFunctionDef) else 'def'

        for decorator in get_only_mark_decorators(funcdef.decorator_list):
            self.add_focused_error(decorator, func_type, funcdef.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        classdef = node

        if classdef.decorator_list:
            for mark in get_only_mark_decorators(classdef.decorator_list):
                self.add_focused_error(mark, 'class', classdef.name)

        for stmt in classdef.body:
            mark = get_pytestmark_assign_value(stmt)
            if not mark:
                self.visit(stmt)
                continue

            for mark in iter_only_mark_pytestmarks(mark):
                self.add_focused_error(mark, 'class', classdef.name)

    def visit_Module(self, node: ast.Module) -> None:
        module = node

        for stmt in module.body:
            mark = get_pytestmark_assign_value(stmt)
            if not mark:
                self.visit(stmt)
                continue

            for mark in iter_only_mark_pytestmarks(mark):
                self.add_focused_error(mark, 'module', '<module>')


def is_only_mark(node: ast.expr) -> bool:
    """Return whether an expression is a pytest.mark.only mark

    >>> parse_decorator = lambda s: ast.parse(s).body[0].decorator_list[0]
    >>> is_only_mark(parse_decorator('@pytest.mark.only\\ndef test_it(): pass'))
    True
    >>> is_only_mark(parse_decorator('@pytest.mark.only()\\ndef test_it(): pass'))
    True
    >>> is_only_mark(parse_decorator('@pytest.mark.muffin\\ndef test_it(): pass'))
    False
    """
    if isinstance(node, ast.Call):
        mark = node.func
    elif isinstance(node, ast.Attribute):
        mark = node
    else:
        return False

    for attr in ('only', 'mark'):
        if not isinstance(mark, ast.Attribute) or mark.attr != attr:
            return False
        mark = mark.value

    return isinstance(mark, ast.Name) and mark.id == 'pytest'


def get_only_mark_decorators(decorators: List[ast.expr]) -> List[ast.expr]:
    return [node for node in decorators if is_only_mark(node)]


def iter_only_mark_pytestmarks(
    pytestmark: Union[ast.expr, ast.List]
) -> List[ast.expr]:
    elements = pytestmark.elts if isinstance(pytestmark, ast.List) else [pytestmark]
    for elt in elements:
        if is_only_mark(elt):
            yield elt


def get_pytestmark_assign_value(stmt: ast.stmt) -> Optional[ast.expr]:
    if isinstance(stmt, ast.Assign):
        if len(stmt.targets) == 1:
            if hasattr(stmt.targets[0], 'elts'):
                targets = stmt.targets[0].elts
                values = getattr(stmt.value, 'elts', None)
                if values is None:
                    values = (stmt.value,) * len(targets)
            else:
                targets = stmt.targets
                values = (stmt.value,)
        else:
            raise AssertionError('when does this happen?')

        for target, value in zip(targets, values):
            if isinstance(target, ast.Name) and target.id == 'pytestmark':
                return value
