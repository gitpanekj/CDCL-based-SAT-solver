from formula import *
from enum import Enum, auto


type Model = list[int]
class Status(Enum):
    SAT = auto()
    UNSAT = auto()
    UNKNOW = auto()


class Solver:
    def solve(self, header, formula) -> tuple[Status, None | Model]:
        return (Status.UNKNOW, None)