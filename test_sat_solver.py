import unittest
from satSolver import dpll

class TestDPLL(unittest.TestCase):

    def test_simple_satisfiable(self):
        # Example: (A)
        # Variable 1 is A
        clauses = [[1]]
        # Initial assignment and history are empty lists
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for clauses: [[1]]")
        self.assertIn(1, assignment, "Expected 1 to be in assignment for clauses: [[1]]")

    def test_simple_unsatisfiable(self):
        # Example: (A) AND (NOT A)
        # Variable 1 is A
        clauses = [[1], [-1]]
        res, assignment = dpll(clauses, [], [])
        self.assertFalse(res, "Expected unsatisfiable for clauses: [[1], [-1]]")

    def test_satisfiable_two_vars_or(self):
        # Example: (A OR B)
        # Variable 1 is A, Variable 2 is B
        clauses = [[1, 2]]
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for clauses: [[1, 2]]")
        # Check that the assignment satisfies the clause (at least one literal is true)
        # For [1, 2], assignment could be [1], [2], [1,2], [1,-2], [-1,2] etc.
        # DPLL might return a minimal assignment, e.g., just [1] or just [2].
        self.assertTrue(any(literal in assignment for literal in clauses[0]), 
                        f"Assignment {assignment} does not satisfy clauses {clauses}")

    def test_satisfiable_two_vars_unit_prop(self):
        # Example: (A) AND (A OR B)
        # Variable 1 is A, Variable 2 is B
        # A must be true from the first clause (unit propagation).
        # Second clause (A OR B) is then satisfied.
        clauses = [[1], [1, 2]]
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for clauses: [[1], [1, 2]]")
        self.assertIn(1, assignment, "Expected 1 to be in assignment due to unit propagation")

    def test_unsatisfiable_complex(self):
        # Example: (A OR B) AND (A OR NOT B) AND (NOT A OR C) AND (NOT A OR NOT C)
        # (A V B) & (A V ~B) implies A must be true.
        # (~A V C) & (~A V ~C) implies ~A must be true.
        # This is a contradiction.
        # Variables: 1=A, 2=B, 3=C
        clauses = [[1, 2], [1, -2], [-1, 3], [-1, -3]]
        res, assignment = dpll(clauses, [], [])
        self.assertFalse(res, "Expected unsatisfiable for clauses: [[1, 2], [1, -2], [-1, 3], [-1, -3]]")

    def test_empty_clauses(self):
        # No clauses means it's satisfiable by definition (vacuously true).
        clauses = []
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for empty clauses list")
        self.assertEqual(assignment, [], "Expected empty assignment for empty clauses list")

    def test_clause_with_empty_clause_inside(self):
        # Contains an empty clause, so unsatisfiable.
        # An empty clause means there's no way to satisfy it.
        clauses = [[1, 2], []]
        res, assignment = dpll(clauses, [], [])
        self.assertFalse(res, "Expected unsatisfiable for clauses list containing an empty clause")

    def test_satisfiable_pure_literal(self):
        # Example: (A or B) and (A or ~C)
        # A is a pure literal. Setting A=true satisfies both.
        # B and C can be anything or not assigned if A is true.
        # 1=A, 2=B, 3=C
        clauses = [[1, 2], [1, -3]]
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for clauses with pure literal: [[1, 2], [1, -3]]")
        self.assertIn(1, assignment, "Expected pure literal 1 to be in assignment")

    def test_satisfiable_complex_case(self):
        # (A or B or ~C) and (B or C or D) and (~A or D) and (~B or ~D)
        # 1=A, 2=B, 3=C, 4=D
        # One possible assignment: A=T, B=F, C=T, D=F (1, -2, 3, -4)
        # Clause 1: (T or F or ~T) = (T or F or F) = T
        # Clause 2: (F or T or F) = T
        # Clause 3: (~T or F) = (F or F) = F -> This assignment doesn't work.
        # Let's try another: A=T, B=F, D=T
        # (1, -2, 4)
        # C1: (T or F or ~C) -> T if ~C, so C=F (-3)  -> (1, -2, -3, 4)
        # C2: (F or F or T) -> T
        # C3: (~T or T) -> T
        # C4: (~F or ~T) -> (T or F) -> T
        # So, (1, -2, -3, 4) should be a solution.
        clauses = [[1, 2, -3], [2, 3, 4], [-1, 4], [-2, -4]]
        res, assignment = dpll(clauses, [], [])
        self.assertTrue(res, "Expected satisfiable for complex clauses: [[1, 2, -3], [2, 3, 4], [-1, 4], [-2, -4]]")
        
        # Verify the assignment satisfies all clauses
        for clause in clauses:
            satisfied_by_clause = False
            for literal in clause:
                if literal in assignment:
                    satisfied_by_clause = True
                    break
            self.assertTrue(satisfied_by_clause, f"Assignment {assignment} does not satisfy clause {clause} in {clauses}")

if __name__ == '__main__':
    unittest.main()
