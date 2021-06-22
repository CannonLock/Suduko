from math import *
import numpy as np

def get_sub_cols(sub_box, indexes):



class SudokuBoard:

    def __init__(self, puzzle=None, verbose=False):
        self.board = np.array([[SudokuSquare((row, col)) for col in range(9)] for row in range(9)])
        if puzzle is not None:
            self.loadPuzzle(puzzle)
        self.verbose = verbose

    def __str__(self):
        board = ""
        for row in self.board:
            board += str([str(x) for x in row]) + "\n"
        return board

    def __getitem__(self, item):
        return self.board[item]

    def __iter__(self):
        return iter(np.array(self.board).reshape((-1)))

    def getBoardArray(self):
        return [[self.board[j][i].getValue() for i in range(9)] for j in range(9)]

    def loadPuzzle(self, values):
        for i in range(9):
            for j in range(9):
                if values[i][j] != 0:
                    self.setSquare(self.board[i][j], values[i][j])

    def setSquare(self, square, value):
        square.setValue(value)

    def knownBoard(self):
        for row in self.board:
            print(map(lambda a: a.getValue(), row))

    def rowSquares(self, row):
        return self.board[row]

    def colSquares(self, col):
        return self.board[:,col]

    def boxSquares(self, row, col):
        """
        :param row: index of row
        :param col: index of col
        :return: list of squares with there indices matching the box above
        """
        squares = []
        box_base_row = (row // 3) * 3
        box_base_col = (col // 3) * 3
        for i in range(9):
            row_index = i // 3 + box_base_row
            col_index = i % 3 + box_base_col

            squares.append(self.board[row_index][col_index])

        return squares

    def get_rows(self):
        return self.board

    def get_cols(self):
        return self.board.transpose()

    def get_boxes(self):
        """
        012
        345
        678
        :return: All of the boxes with indexes above
        """
        boxes = []
        for i in range(3):
            for j in range(3):
                boxes.append(self.boxSquares(i * 3, j * 3))
        return np.array(boxes)

    def get_associated_squares(self, row_index, col_index):
        """
		Gets all the squares that are associated with this index
		i.e. in the same row, col, or box
		:param row_index:
		:param col_index:
		:return: Iterable of squares
		"""
        associated_squares = []

        row = self.rowSquares(row_index)
        associated_squares.extend(row)

        col = self.colSquares(col_index)
        associated_squares.extend(col)

        box = self.boxSquares(row_index, col_index)
        associated_squares.extend(box)

        return associated_squares


class SudokuSquare:

    def __init__(self, index, verbose=False):
        self.possibles = set(range(1, 10))
        self.index = index
        self.verbose = verbose

    def __str__(self):
        return str(self.getValue())

    def __eq__(self, other):
        return self.index == other.index

    def __ne__(self, other):
        return self.index != other.index

    def isSet(self):
        if (len(self.possibles) == 1):
            return True
        return False

    def removePossible(self, value):
        if len(self.possibles) == 1 and value in self.possibles:
            raise Exception("You cannot remove all values from possibles array")
        self.possibles.discard(value)

    def getValue(self):
        if self.isSet():
            value = next(iter(self.possibles))
            return value
        return 0

    def setValue(self, value):
        if value not in self.possibles:
            raise Exception("You cannot make this a value that was deemed not possible")
        self.possibles.clear()
        self.possibles.add(value)
