import ast
import operator


_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


class UnsafeExpression(ValueError):
    pass


def safe_calculate(expression: str) -> float:
    """Evaluate numeric arithmetic only. No names, calls, attributes, or imports."""
    if len(expression) > 200:
        raise UnsafeExpression("Expression is too long.")

    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 12:
                raise UnsafeExpression("Exponent too large.")
            return _BINARY[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](visit(node.operand))
        raise UnsafeExpression(f"Disallowed syntax: {type(node).__name__}")

    result = visit(tree)
    if abs(float(result)) > 1e18:
        raise UnsafeExpression("Result outside allowed range.")
    return float(result)
