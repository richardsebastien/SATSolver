"""
This file contains the function that converts a sudoku puzzle to a SAT problem.
"""


def readSudoku(filename):
    """
    This function reads a Sudoku puzzle from a file.
    """
    import sys # Required for sys.stderr
    sudoku = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) != 9:
                sys.stderr.write(f"Error: Sudoku file {filename} does not contain 9 lines.\n")
                return []
            for line_num, line in enumerate(lines, 1):
                row_values = line.split()
                if len(row_values) != 9:
                    sys.stderr.write(f"Error: Line {line_num} in Sudoku file {filename} does not contain 9 numbers.\n")
                    return []
                try:
                    sudoku.append([int(x) for x in row_values])
                except ValueError:
                    sys.stderr.write(f"Error: Non-integer value found in Sudoku file {filename} at line {line_num}: {line.strip()}\n")
                    return [] # Return empty list on error
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found - {filename}\n")
        return [] # Return empty list on error
    except Exception as e: # Catch any other unexpected errors during file processing
        sys.stderr.write(f"An unexpected error occurred while reading {filename}: {e}\n")
        return [] # Return empty list on error
    return sudoku


def sudokuToSAT(sudoku):
    """
    This function converts a Sudoku puzzle to a SAT problem.
    """
    clauses = []

    def to_var(r, c, v):
        return r * 81 + c * 9 + v + 1

    # Each cell contains at least one number
    for i in range(9):
        for j in range(9):
            clauses.append([to_var(i, j, k) for k in range(9)])

    # Each cell contains at most one number
    for i in range(9):
        for j in range(9):
            for x in range(9):
                for y in range(x + 1, 9):
                    clauses.append([-to_var(i, j, x), -to_var(i, j, y)])

    # Each number appears at least once in each row
    for i in range(9):
        for k in range(9):
            clauses.append([to_var(i, r_j, k) for r_j in range(9)])

    # Each number appears at least once in each column
    for j in range(9):
        for k in range(9):
            clauses.append([to_var(c_i, j, k) for c_i in range(9)])

    # Each number appears at least once in each 3x3 square
    for x in range(3):
        for y in range(3):
            for k in range(9):
                clauses.append(
                    [to_var(s_i, s_j, k) for s_i in range(3 * x, 3 * x + 3) for s_j in range(3 * y, 3 * y + 3)])

    # If a cell is filled, add a clause
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                clauses.append([to_var(i, j, sudoku[i][j] - 1)])

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
