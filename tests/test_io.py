import pathlib

from pyra import io, relations


test_data_dir = pathlib.Path(__file__).parent.joinpath("testdata")


def test_load_csv():
    sch = {
        "id": relations.Integer(),
        "name": relations.String(),
        "score": relations.Float(),
    }
    want = relations.Relation(
        [(1, "test1", 123.8), (2, "test2", 67.3), (3, "test3", 2.3), (4, "test4", 1.0)],
        sch,
    )
    data_file = test_data_dir.joinpath("relation.csv")
    actual = io.load_csv(data_file, sch)
    assert want == actual
