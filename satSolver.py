def read_file(file):
    """
    This function reads the input file and returns a list of clauses.
    """
    clauses = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            clause =[int(x) for x in line.split()]
            clauses.append(clause)
    return clauses

def find_unit(clauses):
    """
    This function finds a unit clause in the list of clauses.
    """
    for clause in clauses:
        if len(clause) == 1:
            return clause[0]


def remove_clause(clauses, unit):
    """
    This function removes the unit clause from the list of clauses.
    """
    new_clauses = []
    for clause in clauses:
        if unit not in clause:
            new_clauses.append(clause)
    return new_clauses

def remove_opposite(clauses, unit):
    """
    This function removes the opposite of the unit clause from the list of clauses.
    """
    new_clauses = []
    for clause in clauses:
        if -unit not in clause:
            new_clauses.append(clause)
        else:
            new_clause = []
            for x in clause:
                if x != -unit:
                    new_clause.append(x)
            new_clauses.append(new_clause)
    return new_clauses

def find_pure(clauses):
    """
    This function finds a pure literal in the list of clauses.
    """
    pure = []
    literals = []
    for clause in clauses:
        for literal in clause:
            if literal not in literals:
                literals.append(literal)
    for literal in literals:
        if -literal not in literals:
            pure.append(literal)
    return pure

def solve(clauses):
    """
    This function solves the SAT problem.
    """
    assignment = []
    while len(clauses) > 0:
        unit = find_unit(clauses)
        print(clauses,unit)
        if unit:
            clauses = remove_clause(clauses, unit)
            clauses = remove_opposite(clauses, unit)
            assignment.append(unit)
        else:
            pure = find_pure(clauses)
            if pure:
                clauses = remove_clause(clauses, pure[0])
                clauses = remove_opposite(clauses, pure[0])
                assignment.append(pure[0])
            else:
                return None
    return assignment