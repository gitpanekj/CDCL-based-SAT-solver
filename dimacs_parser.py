import sys
from formula import *
import re

type VariableNumber = int
type ClauseNumber = int
type Header = tuple[VariableNumber, ClauseNumber]


def parse_clause(line, formula):
    clauses = filter(lambda x: x, line.strip().split(' 0'))
    for c in clauses:
        clause = list(map(int, re.sub(r'\s+', ' ', c).strip(' ').split(' ')))
        formula.append(clause)

def parse_header(line) -> Header:
    variable_number, clause_number = re.sub(r'\s+', ' ', line).strip().split(' ')[2:]
    return (int(variable_number), int(clause_number))



def parse_input(stream) -> tuple[Header, Formula]:
    header: Header = None
    formula: list = []
    for line in stream:
        line = line.lstrip()
        if not line:    continue
        if line[0] == 'c':         # comment
            pass
        elif line[0] == 'p':       # header
            header = parse_header(line)
        elif line[0] == '0':
            break
        elif line[0].isdigit():    # clause
            parse_clause(line, formula)
    
    return (header, formula)