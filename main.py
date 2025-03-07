from dimacs_parser import parse_input
from solver import Solver, Status
import sys

def main() -> int:
    # input
    header, formula = parse_input()
    # solve
    solver = Solver()
    result = solver.solve(header, formula)
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