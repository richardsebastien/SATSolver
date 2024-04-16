"""
This file contains the functions that generate the clauses for the SAT solver.
"""
import random


def generate_clauses(filename, num_vars, num_clauses):
    with open(filename, 'w') as f:
        for i in range(num_clauses):
            clause = []
            for j in range(num_vars):
                if random.randint(0, 1):
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            f.write(' '.join(map(str, clause)) + '\n')
