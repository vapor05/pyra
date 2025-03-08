from dataclasses import dataclass
import enum
import typing


    


class Column:

    def __init__(self, name: str):
        self.name = name

    def __and__(self, other: typing.Any):
        pass

    def __eq__(self, value: typing.Any):
        pass