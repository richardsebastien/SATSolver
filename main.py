"""
@Author: RICHARD Sébastien
@Date: 2024-04-15
@Description: This is the main file for the SAT solver. It will read the input file, and then call the functions
in satSolver.py to solve the SAT problem.
@Input: The input file is a text file with the following format: each line is a clause, and each number is a literal.
@Output: The output is a text file with the following format: the first line is the number of variables,
and the second line is the assignment of the variables.
"""
import sys

from satSolver import read_file, dpll
from clauses import generate_clauses
from sudoku import readSudoku, sudokuToSAT, satToSudoku, printSudoku

if __name__ == '__main__':
    sudoku = readSudoku("testsudoku.txt")
    clauses = sudokuToSAT(sudoku)
    args = sys.argv[1:]
    res, assignment = dpll(clauses, [], [])
    solution = satToSudoku(assignment)
    if res:
        print("This SAT problem is satisfiable.")
        print("The assignment of the variables is:")
        print(list(set(assignment)))  # Show unique values
        printSudoku(sudoku)
    else:
        print("This SAT problem is not satisfiable.")
