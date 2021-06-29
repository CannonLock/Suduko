import unittest
import glob
import numpy as np
from Board.board import SudokuBoard, SudokuSquare
from Solver.solver import SudokuSolver

class Test_Create_A_Puzzle(unittest.TestCase):

    def test_create_a_puzzle_multi(self):
        saved = np.load("./test_puzzles/test_create_a_puzzle_multi.npy")
        test = np.array([[i for i in range(9)] for j in range(9)])

        self.assertTrue(np.allclose(test, saved))

    def test_create_a_puzzle_single(self):
        saved = np.load("./test_puzzles/test_create_a_puzzle_single.npy")
        test = np.array([[i for i in range(9)] for j in range(9)])

        self.assertTrue(np.allclose(test, saved))

class Test_Get_Associated_Squares(unittest.TestCase):

    def setUp(self):
        self.board = SudokuBoard()

    def test_get_associated_squares_all(self):
        for x in range(9):
            for y in range(9):

                squares = self.board.get_associated_squares(y,x)
                calc_indexes = set([i.index for i in squares])

                correct_indexes = [(i,x) for i in range(9)]
                correct_indexes.extend([(y,i) for i in range(9)])
                for i in range(3):
                    correct_indexes.extend([(i + (y//3)*3, j + (x//3)*3) for j in range(3)])
                correct_indexes = set(correct_indexes)

                with self.subTest():
                    self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_2_2(self):
        squares = self.board.get_associated_squares(2,2)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,2) for x in range(9)]
        correct_indexes.extend([(2,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y,x) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_3_4(self):
        squares = self.board.get_associated_squares(3,4)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,4) for x in range(9)]
        correct_indexes.extend([(3,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y+3,x+3) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_5_8(self):
        squares = self.board.get_associated_squares(5,8)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,8) for x in range(9)]
        correct_indexes.extend([(5,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y+3,x+6) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_8_8(self):
        squares = self.board.get_associated_squares(8,8)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,8) for x in range(9)]
        correct_indexes.extend([(8,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y+6,x+6) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_8_0(self):
        squares = self.board.get_associated_squares(8,0)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,0) for x in range(9)]
        correct_indexes.extend([(8,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y+6,x) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

    def test_get_associated_squares_2_4(self):
        squares = self.board.get_associated_squares(2,4)

        calc_indexes = set([x.index for x in squares])

        correct_indexes = [(x,4) for x in range(9)]
        correct_indexes.extend([(2,x) for x in range(9)])
        for y in range(3):
            correct_indexes.extend([(y+0,x+3) for x in range(3)])
        correct_indexes = set(correct_indexes)

        self.assertEqual(calc_indexes, correct_indexes)

class Test_Sudoku_Square(unittest.TestCase):

    def setUp(self):
        self.square = SudokuSquare((0,0))

    def test_get_value(self):
        self.square.setValue(8)
        self.assertEquals(self.square.getValue(), 8)

    def test_equality_true(self):
        self.assertTrue(self.square == self.square)

    def test_equality_false(self):
        self.assertFalse(self.square == SudokuSquare((1,2)))

    def test_inequality_true(self):
        self.assertTrue(self.square != SudokuSquare((1,2)))

    def test_inequality_false(self):
        self.assertFalse(self.square != self.square)

class Test_Sudoku_Board(unittest.TestCase):

    def setUp(self):
        self.board = SudokuBoard()

    def test_get_item(self):
        self.assertEqual(self.board[1][3].index, (1,3))

    def test_get_iter(self):
        all_squares = set(s.index for s in iter(self.board))
        test_all_squares = []
        for i in range(9):
            for j in range(9):
                test_all_squares.append((i,j))
        self.assertEqual(all_squares, set(test_all_squares))

    def test_load(self):
        puzzle = np.load("./test_puzzles/test_2.npy")

        self.board.loadPuzzle(puzzle)
        self.assertTrue(np.allclose(puzzle, np.array(self.board.getBoardArray())))

class Test_Sudoku_Solver_Sole_Candidate(unittest.TestCase):

    def test_sole_candidate_row(self):
        solver = SudokuSolver("./test_puzzles/test_sole_candidate_row.npy")
        solver.sole_candidate()
        self.assertEqual(solver.board[0][0].getValue(), 1)

    def test_sole_candidate_col(self):
        solver = SudokuSolver("./test_puzzles/test_sole_candidate_col.npy")
        solver.sole_candidate()
        self.assertEqual(solver.board[0][0].getValue(), 3) # This is right, I did 3 on accident

    def test_sole_candidate_box(self):
        solver = SudokuSolver("./test_puzzles/test_sole_candidate_box.npy")
        solver.sole_candidate()
        self.assertEqual(solver.board[0][0].getValue(), 1)

    def test_sole_candidate_combo(self):
        solver = SudokuSolver("./test_puzzles/test_sole_candidate_combo.npy")
        solver.sole_candidate()
        self.assertEqual(solver.board[0][0].getValue(), 1)

class Test_Sudoku_Solver_Unique_Candidate(unittest.TestCase):

    def test_unique_candidate_custom_0(self):
        solver = SudokuSolver("./test_puzzles/test_unique_candidate_custom_0.npy")
        solver.sole_candidate() # Have to run this first to narrow down the possibles
        solver.unique_candidate()
        self.assertEqual(4, solver.board[7][0].getValue())

    def test_unique_candidate_custom_1(self):
        solver = SudokuSolver("./test_puzzles/test_unique_candidate_custom_1.npy")
        solver.sole_candidate() # Have to run this first to narrow down the possibles
        solver.unique_candidate()
        self.assertEqual(4, solver.board[2][0].getValue())

class Test_Sudoku_Solver_Block_Column_Interaction(unittest.TestCase):

    def test_custom_1(self):
        solver = SudokuSolver("./test_puzzles/test_block_column_interaction_custom_1.npy")
        solver.sole_candidate()  # Have to run this first to narrow down the possibles
        solver.block_row_interaction()
        possibles = solver.board[4][1].possibles
        self.assertTrue(7 not in possibles)

    def test_custom_2(self):
        solver = SudokuSolver("./test_puzzles/test_block_column_interaction_custom_1.npy")
        solver.sole_candidate()  # Have to run this first to narrow down the possibles
        solver.block_row_interaction()
        possibles = solver.board[4][5].possibles
        self.assertTrue(7 in possibles)

class Test_Sudoku_Solver_Block_Row_Interaction(unittest.TestCase):

    def test_custom_1(self):
        solver = SudokuSolver("./test_puzzles/test_block_row_interaction_custom_1.npy")
        solver.sole_candidate()  # Have to run this first to narrow down the possibles
        solver.block_column_interaction()
        possibles = solver.board[1][4].possibles
        self.assertTrue(7 not in possibles)

    def test_custom_2(self):
        solver = SudokuSolver("./test_puzzles/test_block_row_interaction_custom_1.npy")
        solver.sole_candidate()  # Have to run this first to narrow down the possibles
        solver.block_column_interaction()
        possibles = solver.board[5][4].possibles
        self.assertTrue(7 in possibles)