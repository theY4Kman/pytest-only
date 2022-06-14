from typing import List, Union

from astroid import nodes
from pylint.checkers.base_checker import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


def is_only_mark(node: nodes.NodeNG) -> bool:
    return (
       isinstance(node, nodes.Attribute)
       and node.attrname == 'only'
       and isinstance(node.expr, nodes.Attribute)
       and node.expr.attrname == 'mark'
    )


def get_only_mark_decorators(decorators: nodes.Decorators) -> List[nodes.NodeNG]:
    return [node for node in decorators.nodes if is_only_mark(node)]


def get_only_mark_pytestmarks(
    pytestmark: Union[nodes.AssignName, List[nodes.NodeNG]]
) -> List[nodes.NodeNG]:
    if isinstance(pytestmark, list):
        if len(pytestmark) != 1:
            return []

        pytestmark = pytestmark[0]
        if not isinstance(pytestmark, nodes.AssignName):
            return []

    assigned_stmts = tuple(pytestmark.assigned_stmts())
    if len(assigned_stmts) == 1:
        rhs = assigned_stmts[0]

        if isinstance(rhs, nodes.List):
            all_marks = rhs.elts
        else:
            all_marks = (rhs,)

        return [mark for mark in all_marks if is_only_mark(mark)]


class PytestOnlyMarkChecker(BaseChecker):
    """Check for stray pytest.mark.only decorators"""

    __implements__ = IAstroidChecker

    name = 'pytest-only-mark'
    msgs = {
        'W1650': (
            'Unexpected focused test(s) using pytest.mark.only: %s %s',
            'unexpected-focused',
            'Remove pytest.mark.only from test',
        )
    }

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        funcdef = node

        if not funcdef.decorators:
            return

        func_type = 'async def' if isinstance(funcdef, nodes.AsyncFunctionDef) else 'def'
        for node in get_only_mark_decorators(funcdef.decorators):
            self.add_message('unexpected-focused', args=(func_type, funcdef.name), node=node)

    visit_asyncfunctiondef = visit_functiondef

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        classdef = node

        if classdef.decorators:
            for mark in get_only_mark_decorators(classdef.decorators):
                self.add_message('unexpected-focused', args=('class', classdef.name), node=mark)

        if 'pytestmark' in classdef.locals:
            for mark in get_only_mark_pytestmarks(classdef.locals['pytestmark']):
                self.add_message('unexpected-focused', args=('class', classdef.name), node=mark)

    def visit_module(self, node: nodes.Module) -> None:
        module = node

        if 'pytestmark' in module.locals:
            for mark in get_only_mark_pytestmarks(module.locals['pytestmark']):
                self.add_message('unexpected-focused', args=('module', module.name), node=mark)


def register(linter: PyLinter) -> None:
    linter.register_checker(PytestOnlyMarkChecker(linter))
