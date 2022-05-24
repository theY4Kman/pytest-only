from astroid import nodes
from pylint.checkers.base_checker import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


class MarkOnlyCheckerChecker(BaseChecker):
    """Check for stray pytest.mark.only decorators"""

    __implements__ = IAstroidChecker

    name = "mark-only"
    msgs = {
        "W1650": (
            "Unexpected focused test using pytest.mark.only",
            "unexpected-focused",
            "Remove pytest.mark.only from test",
        )
    }

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Called when a :class:`.nodes.FunctionDef` node is visited.
        See :mod:`astroid` for the description of available nodes.
        """

        # Does it have a decorator?
        if not isinstance(node.decorators, nodes.Decorators):
            return

        # Is it a mark.only decorator?
        mark_only_nodes = [
            _node
            for _node in node.decorators.nodes
            if isinstance(_node, nodes.Attribute)
            and _node.attrname == 'only'
            and isinstance(_node.expr, nodes.Attribute)
            and _node.expr.attrname == 'mark'
        ]

        if len(mark_only_nodes) < 1:
            return

        for node in mark_only_nodes:
            self.add_message("unexpected-focused", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(MarkOnlyCheckerChecker(linter))