def read_file(file):
    """
    This function reads the input file and returns a list of clauses.
    """
    import sys  # Required for sys.stderr
    clauses = []
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                try:
                    clause = [int(x) for x in line.split()]
                    clauses.append(clause)
                except ValueError:
                    sys.stderr.write(f"Error: Non-integer value found in clause in file {file} at line {line_num}: {line.strip()}\n")
                    return [] # Return empty list on error
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found - {file}\n")
        return [] # Return empty list on error
    except Exception as e: # Catch any other unexpected errors during file processing
        sys.stderr.write(f"An unexpected error occurred while reading {file}: {e}\n")
        return [] # Return empty list on error
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
    It returns a list of all pure literals found.
    """
    present_literals = set()
    all_literals_in_clauses = set()

    for clause in clauses:
        for literal in clause:
            present_literals.add(literal)
            all_literals_in_clauses.add(abs(literal))

    pure_literals = []
    for var_abs in all_literals_in_clauses:
        # Check if var_abs is present but -var_abs is not
        if var_abs in present_literals and -var_abs not in present_literals:
            pure_literals.append(var_abs)
        # Check if -var_abs is present but var_abs is not
        elif -var_abs in present_literals and var_abs not in present_literals:
            pure_literals.append(-var_abs)
            
    return pure_literals


def add_clause(clauses, clause):
    """
    This function adds a clause to the list of clauses.
    """
    new_clauses = clauses[:]
    new_clauses.append(clause)
    return new_clauses


def dpll(clauses, assignment, history):
    """
    This function implements the DPLL algorithm to solve the SAT problem.
    It recursively tries to find a satisfying assignment for a given set of clauses.

    Args:
        clauses (list of list of int): The set of clauses, where each clause is a list of literals.
                                      A positive integer represents a variable, and a negative integer
                                      represents its negation.
        assignment (list of int): The current partial assignment of truth values to variables.
        history (list of list of list of int): A list used to store previous states of clauses
                                              to enable backtracking during the search.
    Returns:
        tuple (bool, list of int): A tuple where the first element is True if a satisfying
                                   assignment is found, False otherwise. The second element
                                   is the satisfying assignment if found, or an empty list.
    """
    # Base case 1: All clauses are satisfied.
    # If the list of clauses is empty, it means all original clauses have been satisfied
    # by the current assignment. Thus, the problem is satisfiable.
    if not clauses:
        return True, assignment

    # Base case 2: A clause is empty, meaning unsatisfiable path.
    # If any clause in the list is empty, it means that all literals in that clause
    # have been assigned a value that makes them false. An empty clause cannot be satisfied.
    # This indicates that the current path in the search tree leads to a contradiction.
    if [] in clauses:
        return False, []

    # Unit Propagation:
    # Find a unit clause (a clause with only one literal).
    # A unit clause must be true for the whole CNF to be true.
    # The literal in a unit clause is called a unit literal.
    unit = find_unit(clauses)
    if unit:
        # Save the current state of clauses before modification for potential backtracking.
        history.append(clauses)
        # Remove clauses containing the unit literal (as they are now satisfied).
        new_clauses_after_unit_prop = remove_clause(clauses, unit)
        # Remove the negation of the unit literal from all other clauses (simplification).
        # If -unit is in a clause, that literal becomes false, so it's removed.
        # If this makes a clause empty, it will be caught in the base case above in the recursive call.
        new_clauses_after_unit_prop = remove_opposite(new_clauses_after_unit_prop, unit)
        # Recursively call dpll with the simplified clauses and the unit literal added to the assignment.
        return dpll(new_clauses_after_unit_prop, assignment + [unit], history)

    # Pure Literal Elimination:
    # Find a pure literal (a literal that appears only with one polarity across all clauses).
    # If a literal `l` is pure, all clauses containing `l` can be satisfied by setting `l` to True,
    # without affecting any other clauses negatively (since `-l` does not appear).
    pure_literals = find_pure(clauses) # `find_pure` returns a list of pure literals.
    if pure_literals:
        chosen_pure_literal = pure_literals[0] # Select the first pure literal found.
        # Save the current state of clauses.
        history.append(clauses)
        # Remove clauses containing the chosen pure literal (as they are satisfied by setting it to True).
        new_clauses_after_pure_elim = remove_clause(clauses, chosen_pure_literal)
        # Since it's pure, its negation doesn't exist, so `remove_opposite` might not strictly be
        # necessary here in the same way as for unit propagation, but applying it ensures consistency
        # and handles any edge cases if `find_pure` logic were to change.
        # Given typical pure literal definition, -chosen_pure_literal won't be in any clause.
        new_clauses_after_pure_elim = remove_opposite(new_clauses_after_pure_elim, chosen_pure_literal)
        # Recursively call dpll with the simplified clauses and the pure literal added to the assignment.
        return dpll(new_clauses_after_pure_elim, assignment + [chosen_pure_literal], history)

    # Branching Step (Literal Selection for Splitting):
    # If no unit clauses or pure literals are found, select a literal to branch on.
    # Heuristic: choose the first literal from one of the shortest clauses.
    # This is a common heuristic aiming to satisfy a constrained part of the problem quickly.
    literal_to_branch = min(clauses, key=len)[0]

    # Save the current state of clauses before trying the first branch (literal = True).
    # This is crucial for backtracking if this choice leads to unsatisfiability.
    history.append(list(map(list, clauses))) # Deep copy clauses for history

    # Branch 1: Try assigning the selected literal to True.
    # To do this, we add a new clause `[literal_to_branch]` to the set of clauses.
    # In the next recursive call, `literal_to_branch` will be picked up as a unit clause by `find_unit`.
    # This effectively forces `literal_to_branch` to be True.
    clauses_for_true_branch = add_clause(clauses, [literal_to_branch])
    res, new_assignment = dpll(clauses_for_true_branch, assignment + [literal_to_branch], history)
    if res:
        # If the recursive call returns True, a satisfying assignment is found. Propagate it upwards.
        return res, new_assignment

    # Backtracking: If the first branch (literal_to_branch = True) did not lead to a solution.
    # Restore the clauses to the state before attempting the `literal_to_branch = True` assignment.
    # This is done by popping the saved state from history.
    clauses_before_branching = history.pop()

    # Branch 2: Try assigning the selected literal to False.
    # To do this, we add a new clause `[-literal_to_branch]` to the set of clauses.
    # In the next recursive call, `-literal_to_branch` will be picked up as a unit clause.
    # This effectively forces `literal_to_branch` to be False.
    # Note: We use `clauses_before_branching` here, which is the state *before* the first branch.
    clauses_for_false_branch = add_clause(clauses_before_branching, [-literal_to_branch])
    # No need to save history again here, as this is the second path of a branch; if it fails,
    # this instance of dpll will return False, and backtracking will occur at a higher level if needed.
    return dpll(clauses_for_false_branch, assignment + [-literal_to_branch], history)
