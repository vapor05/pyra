import re
import pytest

from pyra import relations


@pytest.mark.parametrize(
    ["data", "schema", "want"],
    [
        [
            [(1, "a", 10.2), (2, "b", 45.43), (3, "c", 99.9), (4, "d", 1012.3)],
            {
                "id": relations.Integer(),
                "letter": relations.String(),
                "score": relations.Float(),
            },
            relations.ValidateResult(True),
        ],
        [
            [(1, "a", 10.2), (2, "b", 45.43), (3.2, "c", 99.9), (4, "d", 1012.3)],
            {
                "id": relations.Integer(),
                "letter": relations.String(),
                "score": relations.Float(),
            },
            relations.ValidateResult(
                False, relations.ValidateFailInfo(2, "id", 3.2, relations.Integer())
            ),
        ],
        [
            [(1, "a", 10.2), (2, 5, 45.43), (3, "c", 99.9), (4, "d", 1012.3)],
            {
                "id": relations.Integer(),
                "letter": relations.String(),
                "score": relations.Float(),
            },
            relations.ValidateResult(
                False, relations.ValidateFailInfo(1, "letter", 5, relations.String())
            ),
        ],
        [
            [(1, "a", 10.2), (2, "b", 45.43), (3, "c", 99.9), (4, "d", 1012)],
            {
                "id": relations.Integer(),
                "letter": relations.String(),
                "score": relations.Float(),
            },
            relations.ValidateResult(
                False, relations.ValidateFailInfo(3, "score", 1012, relations.Float())
            ),
        ],
    ],
)
def test_validate_tuples(
    data: list[tuple],
    schema: dict[str, relations.DataType],
    want: relations.ValidateResult,
):
    actual = relations._validate_tuples(data, schema)
    assert want == actual


def test_relation():
    r = relations.Relation(
        [(1, "a", 45.5)],
        {
            "id": relations.Integer(),
            "letter": relations.String(),
            "score": relations.Float(),
        },
    )

    bad_data = [(1, "a", 10.2), (2, "b", 45.43), (3, "c", 99.9), (4, "d", 1012)]
    schema = {
        "id": relations.Integer(),
        "letter": relations.String(),
        "score": relations.Float(),
    }
    fi = relations.ValidateFailInfo(3, "score", 1012, relations.Float())

    with pytest.raises(Exception, match=re.escape(f"data doesn't match schema: {fi}")):
        _ = relations.Relation(bad_data, schema)


@pytest.mark.parametrize(
    ["r1", "r2", "want"],
    [
        [
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            True,
        ],
        [
            relations.Relation(
                [(1, "a", 45.5), (2, "b", 3.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            False,
        ],
        [
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "float": relations.Float(),
                },
            ),
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            False,
        ],
        [
            relations.Relation(
                [(1, "a", 45.5)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "float": relations.Float(),
                },
            ),
            relations.Relation(
                [(45.5, 1, "a")],
                {
                    "score": relations.Float(),
                    "id": relations.Integer(),
                    "letter": relations.String(),
                },
            ),
            False,
        ],
    ],
)
def test_relations_eq(r1: relations.Relation, r2: relations.Relation, want: bool):
    actual = r1 == r2
    assert want == actual
