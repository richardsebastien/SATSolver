def read_file(file):
    """
    This function reads the input file and returns a list of clauses.
    """
    clauses = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            clause = [int(x) for x in line.split()]
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

def add_clause(clauses, clause):
    """
    This function adds a clause to the list of clauses.
    """
    new_clauses = clauses[:]
    new_clauses.append(clause)
    return new_clauses


def dpll(clauses):
    """
    This function implements the DPLL algorithm to solve the SAT problem.
    """
    print(clauses)
    if not clauses:
        return True, []
    if [] in clauses:
        return False, []

    unit = find_unit(clauses)
    if unit:
        print("unit", unit)
        new_clauses = remove_clause(clauses, unit)
        new_clauses = remove_opposite(new_clauses, unit)
        return dpll(new_clauses)

    pure = find_pure(clauses)
    if pure:
        print("pure", pure[0])
        new_clauses = remove_clause(clauses, pure[0])
        new_clauses = remove_opposite(new_clauses, pure[0])
        return dpll(new_clauses)

    literal = min(clauses, key=len)[0]  #Litteral with the smallest clause
    print("literal", literal)
    new_clauses = add_clause(clauses, [literal]) #Union of the clauses with the literal
    dpll(new_clauses)
    new_clauses = remove_clause(clauses, literal)
    new_clauses = add_clause(new_clauses, [-literal]) #Union of the clauses with the negation of the literal
    dpll(new_clauses)
    return False, []