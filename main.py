from dimacs_parser import parse_input
from solver import Solver, Status
from formula import Formula, Clause
import sys

def main() -> int:
    # input
    header, _formula = parse_input()
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
            print(model) #TODO: SAT competition format: starts with v, at most 4096 characters, ends with 
            
    
    
    return 0


if __name__ == "__main__":
    sys.exit(main())