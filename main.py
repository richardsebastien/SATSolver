"""
@Author: RICHARD Sébastien
@Date: 2024-04-15
@Description: This is the main file for the SAT solver. It will read the input file, and then call the functions to solve the SAT problem.
@Input: The input file is a text file with the following format: each line is a clause, and each number is a literal.
@Output: The output is a text file with the following format: the first line is the number of variables, and the second line is the assignment of the variables.
"""

def read_file(file):
    clauses = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            clause =[int(x) for x in line.split()]
            clauses.append(clause)
    return clauses

def find_unit(clauses):
    for clause in clauses:
        if len(clause) == 1:
            return clause[0]


def remove_clause(clauses, unit):
    new_clauses = []
    for clause in clauses:
        if unit not in clause:
            new_clauses.append(clause)
    return new_clauses

def remove_opposite(clauses, unit):
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
    pure = []
    for clause in clauses:
        for x in clause:
            if -x not in clauses:
                pure.append(x)
    return pure

if __name__ == '__main__':
    clauses = read_file("clauses.txt")
    print(clauses)