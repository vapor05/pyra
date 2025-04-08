import typing
import pytest

from pyra import column


def test_and_expression():
    and_call = column.and_expression()
    assert and_call(True, True) is True
    assert and_call(True, False) is False


def test_or_expression():
    or_call = column.or_expression()
    assert or_call(True, False) is True
    assert or_call(False, False) is False


def test_equal_expression():
    equal_call = column.equal()
    assert equal_call(1, 1) is True
    assert equal_call("a", "a") is True
    assert equal_call(1, "a") is False


@pytest.mark.parametrize(
    ["left", "right", "op", "row", "schema", "want"],
    [
        [
            column.Column("a"),
            column.Column("b"),
            column.equal(),
            (1, "a", "b"),
            {"id": 0, "a": 1, "b": 2},
            False,
        ],
        [
            column.Column("a"),
            column.Column("b"),
            column.equal(),
            (1, "a", "a"),
            {"id": 0, "a": 1, "b": 2},
            True,
        ],
        [
            column.Column("a"),
            12.5,
            column.equal(),
            (1, "a", "b"),
            {"id": 0, "a": 1, "b": 2},
            False,
        ],
        [
            column.Column("a"),
            12.5,
            column.equal(),
            (1, 12.5, "b"),
            {"id": 0, "a": 1, "b": 2},
            True,
        ],
    ],
)
def test_expression(
    left: column.Column | typing.Any,
    right: column.Column | typing.Any,
    op: column.Operator,
    row: tuple,
    schema: dict[str, int],
    want: bool,
):
    expr = column.Expression(left, op, right)
    actual = expr(row, schema)
    assert want == actual
