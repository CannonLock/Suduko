import numpy as np
from Board.board import SudokuBoard, remove_possibles


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
        box = np.array(box).reshape((3,3))

        options = set(range(3))

        for index in range(3):
            diff_indexes = options.difference([index])

            # Get the other columns possible sets
            diff_squares = box[:,list(diff_indexes)].flatten()
            diff_possibles = set()
            [diff_possibles.update(x.possibles) for x in diff_squares]

            # Get this columns possible set
            squares = box[:,index].flatten()
            possibles = set()
            [possibles.update(x.possibles) for x in squares]

            # Check if there is a value in this box column not in the others
            difference = possibles.difference(diff_possibles)
            if len(difference) != 0:
                col_index = squares[0].index[1]

                # For each value only possible in this col remove from the other cols
                for value in difference:
                    col_squares = self.board.colSquares(col_index)
                    remove_possibles(col_squares, value, squares)

    def block_column_interaction(self):
        all_boxes = self.board.get_boxes()
        for box in all_boxes:
            self.block_column_interaction_helper(box)

    def block_row_interaction_helper(self, box):
        box = np.array(box).reshape((3,3))

        options = set(range(3))

        for index in range(3):
            diff_indexes = options.difference([index])

            # Get the other columns possible sets
            diff_squares = box[list(diff_indexes)].flatten()
            diff_possibles = set()
            [diff_possibles.update(x.possibles) for x in diff_squares]

            # Get this columns possible set
            squares = box[index,:].flatten()
            possibles = set()
            [possibles.update(x.possibles) for x in squares]

            # Check if there is a value in this box column not in the others
            difference = possibles.difference(diff_possibles)
            if len(difference) != 0:
                row_index = squares[0].index[0]

                # For each value only possible in this col remove from the other cols
                for value in difference:
                    row_squares = self.board.rowSquares(row_index)
                    remove_possibles(row_squares, value, squares)

    def block_row_interaction(self):
        all_boxes = self.board.get_boxes()
        for box in all_boxes:
            self.block_row_interaction_helper(box)

    def block_block_col_helper(self, box_0, box_1):

        options = set(range(3))

        for col in range(3):
            comp_cols = options.difference([col])
            diff_squares =


    def block_block_row_helper(self, box_0, box_1):


    def block_block_interaction_helper(self, box_0, box_1):
        box_0 = np.array(box_0).reshape((3,3))
        box_1 = np.array(box_1).reshape((3, 3))

        # If these boxes are in the same row
        if box_0[0][0].index[0] != box_1[0][0].index[0]:
            self.block_block_row_helper(box_0, box_1)

        # If these boxes are in the same column
        if box_0[0][0].index[1] != box_1[0][0].index[1]:
            self.block_block_col_helper(box_0, box_1)


    def block_block_interaction(self):
        all_boxes = self.board.get_boxes()
        for box_0 in all_boxes:
            for box_1 in all_boxes:
                self.block_block_interaction_helper(box_0, box_1)