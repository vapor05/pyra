import pathlib
import csv

from pyra import relations


def load_csv(
    file: pathlib.Path, schema: dict[str, relations.DataType]
) -> relations.Relation:
    with open(file, "r") as f:
        csv_r = csv.reader(f)
        tuples = []
        header = False
        dts = list(schema.values())

        for r in csv_r:
            if not header:
                header = True
            else:
                tuples.append(tuple(dts[i].cast(e) for i, e in enumerate(r)))

    return relations.Relation(tuples, schema)
