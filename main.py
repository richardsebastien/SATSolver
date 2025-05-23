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
# from clauses import generate_clauses # This import is no longer needed
from sudoku import readSudoku, sudokuToSAT, satToSudoku, printSudoku

if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        # Handle CNF file from command line
        cnf_file_path = args[0]
        try:
            clauses = read_file(cnf_file_path)
            res, assignment = dpll(clauses, [], [])
            if res:
                print(f"The SAT problem from {cnf_file_path} is satisfiable.")
                print("The assignment of the variables is:")
                print(list(set(assignment)))
            else:
                print(f"The SAT problem from {cnf_file_path} is not satisfiable.")
        except FileNotFoundError:
            print(f"Error: File not found - {cnf_file_path}")
        except Exception as e:
            print(f"An error occurred while processing {cnf_file_path}: {e}")
    else:
        # Default to Sudoku solver
        print("No CNF file provided. Solving the default Sudoku puzzle.")
        sudoku_puzzle = readSudoku("testsudoku.txt") # Renamed to avoid conflict
        clauses = sudokuToSAT(sudoku_puzzle)
        res, assignment = dpll(clauses, [], [])
        if res:
            print("Sudoku puzzle is satisfiable.")
            solution = satToSudoku(assignment)
            print("The solution for the Sudoku is:")
            printSudoku(solution)
        else:
            print("Sudoku puzzle is not satisfiable.")
