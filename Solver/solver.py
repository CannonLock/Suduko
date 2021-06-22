import numpy as np
from Board.board import SudokuBoard


def create_a_puzzle():
    option = input("Choose 1 for single line entry, 2 for multiline entry:\n")
    if int(option) == 1:
        array = input("Enter single line array:\n")
    elif int(option) == 2:
        array = ""
        array += input("Enter Multi Line array:\n")
        for i in range(8):
            array += input()
    file_name = input("File name:\n")
    int_array = np.array(list(array)).reshape(9, 9).astype(int)
    np.save(file_name, int_array)

    return int_array


class SudokuSolver:

    def __init__(self, puzzle=None):
        if puzzle == None:
            puzzle = create_a_puzzle()
        elif isinstance(puzzle, str):
            puzzle = np.load(puzzle)

        self.board = SudokuBoard(puzzle)

    def __str__(self):
        return str(self.board)

    def sole_candidate_helper(self, c_square):
        """
        Removes this values as a possible for all square groups associated
        :param row: row index
        :param col: col index
        :param val: value to remove
        """
        a_squares = self.board.get_associated_squares(*c_square.index)

        for a_square in a_squares:
            if a_square != c_square:
                a_square.removePossible(c_square.getValue())

    def sole_candidate(self):
        all_squares = iter(self.board)
        for square in all_squares:
            if square.isSet():
                self.sole_candidate_helper(square)

    def unique_candidate_helper(self, square, c_squares):

        possibles = square.possibles

        c_possibles = set()
        for c_square in c_squares:
            if c_square != square:
                c_possibles = c_possibles.union(c_square.possibles)

        difference = possibles.difference(c_possibles)
        if len(difference) == 1:
            square.setValue(next(iter(difference)))

    def unique_candidate(self):
        all_squares = iter(self.board)
        for square in all_squares:

            row_squares = self.board.rowSquares(square.index[0])
            self.unique_candidate_helper(square, row_squares)

            col_squares = self.board.colSquares(square.index[1])
            self.unique_candidate_helper(square, col_squares)

            box_squares = self.board.boxSquares(*square.index)
            self.unique_candidate_helper(square, box_squares)

    def block_column_interaction_helper(self, box):
        box = np.array(box).reshape((3,3)).tolist()

        options = set([1,2,3])


        for current_index in range(3):
            current_col_set = set()
            for square in box[:,current_index]:
                current_col_set = current_col_set.union(square.possibles)

            other_cols_set = set()
            for other_index in options.difference(current_index):
                for square in box[:,other_index]:
                    other_cols_set = other_cols_set.union(square.possibles)

            for diff_value in current_col_set.difference(other_cols_set):




            for other

            c_col =



    def block_column_interaction(self):
        all_boxes = self.board.get_boxes()
        for box in all_boxes:
            self.block_column_interaction_helper(box)
