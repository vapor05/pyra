import typing

from dataclasses import dataclass

from pyra import column


class DataType(typing.Protocol):

    def is_type(self, data: typing.Any) -> bool: ...

    def cast(self, data: typing.Any) -> typing.Any: ...

    def __eq__(self, value):
        return isinstance(value, self.__class__)

    def __repr__(self) -> str:
        return self.__class__.__name__


class String(DataType):

    def is_type(self, data: typing.Any) -> bool:
        return isinstance(data, str)

    def cast(self, data: typing.Any) -> str:
        return str(data)


class Integer(DataType):

    def is_type(self, data: typing.Any) -> bool:
        return isinstance(data, int)

    def cast(self, data: typing.Any) -> int:
        return int(data)


class Float(DataType):

    def is_type(self, data: typing.Any) -> bool:
        return isinstance(data, float)

    def cast(self, data: typing.Any) -> float:
        return float(data)


@dataclass(slots=True, frozen=True)
class ValidateFailInfo:
    row: int
    column: str
    value: typing.Any
    expected: DataType


@dataclass(slots=True, frozen=True)
class ValidateResult:
    valid: bool
    fail_info: ValidateFailInfo | None = None


@dataclass(slots=True, frozen=True)
class SchemaColumn:
    index: int
    data_type: DataType


def _validate_tuples(data: list[tuple], schema: dict[str, DataType]) -> ValidateResult:

    for i, t in enumerate(data):
        for j, sch in enumerate(schema.items()):
            c, dt = sch

            if not dt.is_type(t[j]):
                return ValidateResult(
                    valid=False,
                    fail_info=ValidateFailInfo(
                        row=i, column=c, value=t[j], expected=dt
                    ),
                )

    return ValidateResult(True)


class Relation:

    def __init__(self, data: list[tuple], schema: dict[str, DataType]):
        schema_info = _validate_tuples(data, schema)

        if not schema_info.valid:
            raise Exception(f"data doesn't match schema: {schema_info.fail_info}")

        self.schema = {
            j[0]: SchemaColumn(i, j[1]) for i, j in enumerate(schema.items())
        }
        self._data = data

    def projection(self, *columns: str) -> "Relation":
        if not all([c in self.schema for c in columns]):
            raise Exception("column not found")

        new_sch = {c: self.schema[c].data_type for c in columns}
        indexes = [self.schema[c].index for c in columns]
        new_data = [tuple([t[i] for i in indexes]) for t in self._data]
        return Relation(new_data, new_sch)

    def selection(self, cond: column.Expression) -> "Relation":
        schema_ind = {n: i for i, n in enumerate(self.schema.keys())}
        new_data = [r for r in self._data if cond(r, schema_ind)]
        return Relation(new_data, self._get_schema())

    def join(self, rr: "Relation", on: str) -> "Relation":
        new_data = []
        left_on_pos = self.schema[on].index
        right_on_pos = rr.schema[on].index

        for l in self._data:
            left_on = l[left_on_pos]

            for r in rr._data:
                right_on = r[right_on_pos]

                if left_on == right_on:
                    new_tup = (
                        (left_on,)
                        + tuple(e for i, e in enumerate(l) if i != left_on_pos)
                        + tuple(e for i, e in enumerate(r) if i != right_on_pos)
                    )
                    new_data.append(new_tup)

        new_sch = {on: self.schema[on].data_type}
        new_sch.update({c: dt for c, dt in self._get_schema().items() if c != on})

        for rc, rdt in rr._get_schema().items():
            if rc == on:
                continue

            if rc in new_sch:
                rc = f"{rc}_right"

            new_sch[rc] = rdt

        return Relation(new_data, new_sch)

    def _get_schema(self) -> dict[str, DataType]:
        return {c: i.data_type for c, i in self.schema.items()}

    def __eq__(self, value: typing.Any):
        if not isinstance(value, Relation):
            return False

        return self.schema == value.schema and self._data == value._data

    def __repr__(self) -> str:
        s = {c: i.data_type for c, i in self.schema.items()}
        return f"schema: {s}\ndata: {self._data}"
