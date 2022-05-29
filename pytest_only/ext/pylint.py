from astroid import nodes
from pylint.checkers.base_checker import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


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
        """Called when a :class:`.nodes.FunctionDef` node is visited.
        See :mod:`astroid` for the description of available nodes.
        """
        funcdef = node

        # Does it have a decorator?
        if not funcdef.decorators:
            return

        # Is it a mark.only decorator?
        mark_only_nodes = [
            node
            for node in funcdef.decorators.nodes
            if isinstance(node, nodes.Attribute)
            and node.attrname == 'only'
            and isinstance(node.expr, nodes.Attribute)
            and node.expr.attrname == 'mark'
        ]

        for node in mark_only_nodes:
            self.add_message('unexpected-focused', args=('def', funcdef.name), node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(PytestOnlyMarkChecker(linter))
