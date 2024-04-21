"""
This file contains the function that converts a sudoku puzzle to a SAT problem.
"""


def readSudoku(filename):
    """
    This function reads a Sudoku puzzle from a file.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        sudoku = []
        for line in lines:
            sudoku.append([int(x) for x in line.split()])
    f.close()
    return sudoku


def sudokuToSAT(sudoku):
    """
    This function converts a Sudoku puzzle to a SAT problem.
    """
    clauses = []

    # Each cell contains at least one number
    for i in range(9):
        for j in range(9):
            clauses.append([(i * 9 + j * 9 + k + 1) for k in range(9)])

    # Each cell contains at most one number
    for i in range(9):
        for j in range(9):
            for x in range(9):
                for y in range(x + 1, 9):
                    clauses.append([-(i * 9 + j * 9 + x + 1), -(i * 9 + j * 9 + y + 1)])

    # Each number appears at least once in each row
    for i in range(9):
        for k in range(9):
            clauses.append([(i * 9 + j * 9 + k + 1) for j in range(9)])

    # Each number appears at least once in each column
    for j in range(9):
        for k in range(9):
            clauses.append([(i * 9 + j * 9 + k + 1) for i in range(9)])

    # Each number appears at least once in each 3x3 square
    for x in range(3):
        for y in range(3):
            for k in range(9):
                clauses.append(
                    [(i * 9 + j * 9 + k + 1) for i in range(3 * x, 3 * x + 3) for j in range(3 * y, 3 * y + 3)])

    # If a cell is filled, add a clause
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                clauses.append([(i * 9 + j * 9 + sudoku[i][j])])

    return clauses


def satToSudoku(assignment):
    """
    This function converts a SAT assignment to a Sudoku puzzle.
    """
    # Create an empty Sudoku grid
    sudoku = [[0 for _ in range(9)] for _ in range(9)]

    # For each variable in the assignment
    for var in assignment:
        # Ignore negative variables
        if var > 0:
            # Convert the variable to cell indices and value
            var -= 1
            k = var % 9
            j = (var // 9) % 9
            i = var // 81

            # Fill the corresponding cell in the Sudoku grid
            sudoku[i][j] = k + 1

    return sudoku


def printSudoku(sudoku):
    """
    This function prints a Sudoku puzzle to the console.
    """
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            print(sudoku[i][j], end=" ")
        print()
