from typing import Optional, Sequence
from dimacs_parser import parse_input
from solver import Solver, Status
from formula import Formula, Clause
import sys
from pathlib import Path

def main(argv: Optional[Sequence[str]] = None) -> int:
    stream = sys.stdin
    if len(argv) > 1:
        try:
            stream = open(argv[1], "r")
        except OSError:
            print(f"Failed to open input file {argv[1]}", file=sys.stderr)
            return 1
        
    # input
    header, _formula = parse_input(stream)
    stream.close()
    formula = Formula(header[0])
    for c in _formula:
        formula.append(Clause(c))

    # solve
    solver = Solver()
    result = solver.solve(formula)
    # output
    match result:
        case (Status.UNKNOW, _):
            print("s UNKNOWN")
        case (Status.UNSAT, _):
            print("s UNSATISFIABLE")
        case (Status.SAT, model):
            print("s SATISFIABLE")
            print("v ", *model, "0")
            
    
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))