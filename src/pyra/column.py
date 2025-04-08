import typing


Operator = typing.Callable[["Expression", "Expression"], bool]


def and_expression() -> Operator:
    def call(left: typing.Any, right: typing.Any) -> bool:
        return left and right

    return call


def or_expression() -> Operator:
    def call(left: typing.Any, right: typing.Any) -> bool:
        return left or right

    return call


def equal() -> Operator:
    def call(left: typing.Any, right: typing.Any) -> bool:
        return left == right

    return call


class Expression:

    def __init__(
        self,
        left: "Column | typing.Any",
        operator: Operator,
        right: "Column | typing.Any",
    ):
        self.left = left
        self.operator = operator
        self.right = right

    def __and__(self, other: "Expression") -> "Expression":
        return Expression(self, and_expression(), other)

    def __or__(self, other: "Expression") -> "Expression":
        return Expression(self, or_expression(), other)

    def __call__(self, row: tuple, schema: dict[str, int]) -> bool:
        if isinstance(self.left, Column):
            left_value = row[schema[self.left.name]]
        elif isinstance(self.left, Expression):
            left_value = self.left(row, schema)
        else:
            left_value = self.left

        if isinstance(self.right, Column):
            right_value = row[schema[self.right.name]]
        elif isinstance(self.left, Expression):
            right_value = self.right(row, schema)
        else:
            right_value = self.right

        return self.operator(left_value, right_value)


class Column:

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, value: typing.Any) -> Expression:
        return Expression(self, equal(), value)
