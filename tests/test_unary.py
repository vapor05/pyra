import pytest

from pyra import relations


@pytest.mark.parametrize(
    ["in_r", "cols", "want"],
    [
        [
            relations.Relation(
                [(1, "a", 12.4), (2, "b", 3.4)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            ["id", "letter", "score"],
            relations.Relation(
                [(1, "a", 12.4), (2, "b", 3.4)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
        ],
        [
            relations.Relation(
                [(1, "a", 12.4), (2, "b", 3.4)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            ["letter", "score"],
            relations.Relation(
                [("a", 12.4), ("b", 3.4)],
                {
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
        ],
        [
            relations.Relation(
                [(1, "a", 12.4), (2, "b", 3.4)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            ["score"],
            relations.Relation(
                [(12.4,), (3.4,)],
                {
                    "score": relations.Float(),
                },
            ),
        ],
        [
            relations.Relation(
                [(1, "a", 12.4), (2, "b", 3.4)],
                {
                    "id": relations.Integer(),
                    "letter": relations.String(),
                    "score": relations.Float(),
                },
            ),
            ["score", "id", "letter"],
            relations.Relation(
                [(12.4, 1, "a"), (3.4, 2, "b")],
                {
                    "score": relations.Float(),
                    "id": relations.Integer(),
                    "letter": relations.String(),
                },
            ),
        ],
    ],
    ids=["project_all", "project_some", "project_one", "project_new_order"],
)
def test_projection(
    in_r: relations.Relation, cols: list[str], want: relations.Relation
):
    actual = in_r.projection(*cols)
    assert want == actual
