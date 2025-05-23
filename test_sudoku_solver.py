import unittest
from sudoku import readSudoku, sudokuToSAT, satToSudoku, printSudoku
from satSolver import dpll

# Helper function to check if a Sudoku grid is solved correctly
def is_sudoku_solved(grid):
    if not grid or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False # Should be a 9x9 grid

    # Check rows and columns
    for i in range(9):
        row_vals = set()
        col_vals = set()
        for j in range(9):
            # Check if cell value is valid (1-9)
            if not isinstance(grid[i][j], int) or not (1 <= grid[i][j] <= 9): return False
            if not isinstance(grid[j][i], int) or not (1 <= grid[j][i] <= 9): return False # Check column cell simultaneously
            row_vals.add(grid[i][j])
            col_vals.add(grid[j][i])
        if len(row_vals) != 9 or len(col_vals) != 9:
            return False

    # Check 3x3 subgrids
    for r_offset in range(0, 9, 3):
        for c_offset in range(0, 9, 3):
            box_vals = set()
            for i in range(3):
                for j in range(3):
                    # Check cell value is valid (1-9) before adding to set
                    if not isinstance(grid[r_offset + i][c_offset + j], int) or not (1 <= grid[r_offset + i][c_offset + j] <= 9): return False
                    box_vals.add(grid[r_offset + i][c_offset + j])
            if len(box_vals) != 9:
                return False
    return True

class TestSudokuSolver(unittest.TestCase):

    def test_sudoku_to_sat_basic_clauses(self):
        # A very simple 9x9 Sudoku, e.g., one pre-filled cell
        # This test focuses on the encoding, not solving.
        # Variable encoding helper (consistent with sudoku.py)
        def to_var(r, c, v_idx): # v_idx is 0-8 for values 1-9
            return r * 81 + c * 9 + v_idx + 1

        sudoku_puzzle = [[0 for _ in range(9)] for _ in range(9)]
        sudoku_puzzle[0][0] = 1 # Pre-fill (0,0) with 1 (value_idx 0)
        
        clauses = sudokuToSAT(sudoku_puzzle)
        
        # Check for pre-filled cell clause: var(0,0,1) must be true
        # Digit 1 means index 0 for k in to_var
        self.assertIn([to_var(0, 0, 0)], clauses, "Pre-filled cell clause missing or incorrect.")

        # Check "at least one number in cell (8,8)"
        # This means (var(8,8,1) OR var(8,8,2) OR ... OR var(8,8,9)) must be true
        # Digit k (1-9) means index k-1 for to_var
        cell_8_8_clauses = [to_var(8, 8, k_idx) for k_idx in range(9)]
        self.assertIn(cell_8_8_clauses, clauses, "At-least-one-number-in-cell clause missing or incorrect for (8,8).")

        # Check "cell (0,1) contains at most one number"
        # e.g., NOT (var(0,1,value1_idx) AND var(0,1,value2_idx)) must be true
        # which is (-var(0,1,value1_idx) OR -var(0,1,value2_idx))
        # For x=value_idx 0 (digit 1), y=value_idx 1 (digit 2)
        at_most_one_clause_example = [-to_var(0, 1, 0), -to_var(0, 1, 1)] # Not (val 1 and val 2 in cell 0,1)
        
        # We need to check if ANY such pair exists for cell (0,1) as the order of literals in the clause might vary.
        # However, the problem statement's example is specific. Let's check for that specific one.
        # A more robust check would be to generate all such pairs for a cell and see if they are present.
        # For this test, sticking to the example from the prompt.
        self.assertIn(at_most_one_clause_example, clauses, "At-most-one-number-in-cell clause missing or incorrect for (0,1) values 1 and 2.")


    def test_solve_simple_sudoku(self):
        # Using the standard example puzzle provided in the prompt
        simple_sudoku = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        clauses = sudokuToSAT(simple_sudoku)
        res, assignment = dpll(clauses, [], []) # Assuming history starts empty for a new problem
        
        self.assertTrue(res, "The simple Sudoku puzzle should be satisfiable.")
        
        solution_grid = satToSudoku(assignment)
        
        # print("\nAttempted solution for simple_sudoku:")
        # printSudoku(solution_grid) # For debugging the test

        self.assertTrue(is_sudoku_solved(solution_grid), 
                        "The solved grid does not satisfy Sudoku rules. Check `is_sudoku_solved` or the solver.")

        # Verifying against the known solution for this specific puzzle
        simple_sudoku_solution = [
            [5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]
        ]
        self.assertEqual(solution_grid, simple_sudoku_solution, "The solved Sudoku grid does not match the known correct solution.")


if __name__ == '__main__':
    unittest.main()
