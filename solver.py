from formula import *
from enum import Enum, auto
from dimacs_parser import Header

type Model = dict[Literal, TruthValue]
class Status(Enum):
    SAT = auto()
    UNSAT = auto()
    UNKNOW = auto()


class Solver:
    def __init__(self):
        self.formula: Formula = None
        self.trail: list[int] = []
        self.decisions: list[int] = []
    
    def __decide(self, literal: Literal) -> None:
        """Assign truth_value to a literal.
           A truth value is represented by sign, - false, + truth.
           This decision is flipped to the oposite truth_value
           when the decisison is reached during backtracking.
        """
        self.__assign(literal)                   # assign
        self.decisions.append(len(self.trail)-1) # store the decision idx
        
    def __assign(self, literal: Literal) -> bool:
        """Assign truth_value to a literal.
           A truth value is represented by sign, - false, + truth.
           This decision is NOT flipped to the oposite truth_value
           when the decisison is reached during backtracking.
        """
        conflict = self.formula.assign(literal)
        self.trail.append(literal)
        return conflict
        

    def __backtrack(self) -> bool:
        """Remove all the truth assignment up to the previous decision and
           flip the decision assignment to the oposite truth value.
        """
        last_decision_idx = self.decisions.pop() # remove the decision
        while last_decision_idx < len(self.trail):
            literal = self.trail.pop()
            self.formula.clear_assignment(literal)
        
        self.__assign(-literal)
        
    def __unit_propagate(self) -> bool:
        """Perform unit propagation until
           a unit propagatino can be performed and
           a conflict is not detected after the assignment.
        """
        while len(self.formula.unprocessed_unit_propagations) > 0:
            propagated_literal = self.formula.unprocessed_unit_propagations.popleft()
            correctly_assigned = self.__assign(propagated_literal) # set propagated literal to truth
            if not correctly_assigned:
                return False

        return True # no conflict occured or no literal was propagated
    
    def solve(self, formula: Formula) -> tuple[Status, None | Model]:
        self.formula = formula
        if not self.__unit_propagate():
            return (Status.UNSAT, None)
        
        while literal:=self.formula.next_unassigned_variable:
            self.__decide(-literal) # by default set to False

            while not self.__unit_propagate(): # while unit propagation lead to a conflict
                if len(self.decisions) == 0: # no more decision to flip
                    return (Status.UNSAT, None)
                
                self.__backtrack()
            

        return (Status.SAT, self.formula.assignment_map)