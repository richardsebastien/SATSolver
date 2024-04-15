"""
@Author: RICHARD Sébastien
@Date: 2024-04-15
@Description: This is the main file for the SAT solver. It will read the input file, and then call the functions in satSolver.py to solve the SAT problem.
@Input: The input file is a text file with the following format: each line is a clause, and each number is a literal.
@Output: The output is a text file with the following format: the first line is the number of variables, and the second line is the assignment of the variables.
"""
import sys

from satSolver import read_file, solve

if __name__ == '__main__':
    args = sys.argv[1:]
    clauses = read_file(args[0])
    print(solve(clauses))
