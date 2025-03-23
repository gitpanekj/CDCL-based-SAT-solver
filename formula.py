from typing import Iterable
from enum import Enum, auto
from collections import deque, defaultdict

class ClauseStatus(Enum):
    UNDETERMINED = auto()
    SATISFIED = auto() 
    CONFLICT = auto()
    UNIT_CLAUSE = auto()

class EmptyClauseException(Exception):
    def __init__(self, msg: str) -> None:
        msg = f"{self.__class__.__name__}: {msg}."
        super().__init__(msg)
        

type Literal = int
type TruthValue = int

class Clause(list[Literal]):
    def __init__(self, iterable: Iterable[int], /) -> None:
        if (len(iterable) == 0):
            raise EmptyClauseException("Cannot create empty clause")
        
        super().__init__(iterable)
        self.watch_indexes: list[int] = [0, len(iterable)-1]
    
    @property
    def watched_literal_1(self):
        literal_idx = self.watch_indexes[0]
        return self[literal_idx]
    
    @property
    def watched_literal_2(self):
        literal_idx = self.watch_indexes[1]
        return self[literal_idx]
            
    
    def update_watched_literals(self, assignment) -> tuple[ClauseStatus, Literal]:
        udpated_watch = 0 if assignment[abs(self.watched_literal_1) - 1] != 0 else 1
        stable_watch = abs(udpated_watch - 1)
        for idx, literal in enumerate(self):
            if assignment[abs(literal)-1] == literal:
                return (ClauseStatus.SATISFIED, None)
            
            if assignment[abs(literal)-1] == 0 and idx != self.watch_indexes[stable_watch]:
                self.watch_indexes[udpated_watch] = idx
                return (ClauseStatus.UNDETERMINED, literal) # new watched literal

        # no other literal can be watched
        return (ClauseStatus.UNIT_CLAUSE, self[self.watch_indexes[stable_watch]]) # unit propagated literal


class Formula(list[Clause]):
    def __init__(self, nvars: int):
        self.assignment_map = [0 for _ in range(nvars)]
        self.unassigned_variables: set[int] = set((i for i in range(1, nvars+1)))
        self.watched_literal_clauses: defaultdict[Literal, set[Clause]] = defaultdict(set)
        self.unprocessed_unit_propagations: deque = deque()
    
        
    @property
    def next_unassigned_variable(self):
        if len(self.unassigned_variables) > 0:
            return self.unassigned_variables.pop()
        return 0
         
    def assign(self, literal) -> bool: # conflict
        if self.assignment_map[abs(literal)-1] == -literal:
            return False # confclit
        
        self.assignment_map[abs(literal)-1] = literal
        
        
        removed_clauses = set()
        for clause_idx in self.watched_literal_clauses[-literal]:
            clause = self[clause_idx]
            clause_status, __literal = clause.update_watched_literals(self.assignment_map)
            
            if clause_status == ClauseStatus.UNDETERMINED: # watches were moved
                removed_clauses.add(clause_idx)
                self.watched_literal_clauses[__literal].add(clause_idx)                
            elif clause_status == ClauseStatus.UNIT_CLAUSE:  # unit clause
                self.unprocessed_unit_propagations.append(__literal)
        
        # remove clauses from the set
        self.watched_literal_clauses[-literal].difference_update(removed_clauses)
        
    
        return True
        
    def clear_assignment(self, literal):
        self.assignment_map[abs(literal)-1] = 0
        self.unassigned_variables.add(abs(literal))
        
    
    def append(self, clause: Clause):
        super().append(clause)
                
        if len(clause) == 1: # always unit clause
            # unit propagation of these literals will be perfomed
            # before the first decision therefore
            # the assignment of these clauses cannot be flipped
            self.unprocessed_unit_propagations.append(clause[0])
            return
        
        # NOTE no unit clause reaches watched literal initialization
        w1, w2 = clause.watched_literal_1, clause.watched_literal_2
        clause_idx = len(self)-1
        w1_watched_clauses = self.watched_literal_clauses[w1]
        w2_watched_clauses = self.watched_literal_clauses[w2]
        w1_watched_clauses.add(clause_idx)
        w2_watched_clauses.add(clause_idx)