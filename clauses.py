"""
This file contains the functions that generate the clauses for the SAT solver.
"""
import random


def generate_clauses(filename, num_vars, num_clauses):
    with open(filename, 'w') as f:
        for i in range(num_clauses):
            clause = []
            for j in range(random.randint(1, num_vars)):
                literal = random.randint(1, num_vars)
                if random.randint(0, 1):
                    literal = -literal
                clause.append(literal)
            f.write(' '.join(map(str, clause)) + '\n')
    f.close()

generate_clauses("testgenerate.txt", 1000, 300)
