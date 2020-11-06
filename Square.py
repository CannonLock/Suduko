def coordinatesToBoxIndex(row, col):
	return (row // 3)*3 + (col // 3)

class SudokuSquare:

	def __init__(self, index):
		self.possibles = set(range(1, 10))
		self.index = index

	def isSet(self):
		if(len(self.possibles) == 1):
			return True
		return False

	def removePossible(self, value):
		if len(self.possibles) == 1:
			raise Exception("You cannot remove all values from possibles array")
		self.possibles.discard(value)

	def getValue(self):
		if self.isSet():
			value = self.possibles.pop()
			self.add(value)
			return value
		return 0

	def setValue(self, value):
		if value not in self.possibles:
			raise Exception("You cannot make this a value that was deemed not possible")
		self.possibles.clear()
		self.possibles.add(value)

class SudokuBoard:

	def __init__(self):
		self.board = [[SudokuSquare((row, col)) for col in range(9)] for row in range(9)]

	def setSquare(self, square, value):
		rowIndex, colIndex = square.index
		self.removeValueFromPossibles(rowIndex, colIndex, value)

	def knownBoard(self):
		for row in self.board:
			print(map(lambda a : a.getValue(), row))

	def rowSquares(self, row, indexLess = True):
		squares = []
		for i in range(9):
			if indexLess:
				squares.append(self.board[row][i])
			else:
				squares.append(((row, i), self.board[row][i]))
		return squares

	def colSquares(self, col, indexLess = True):
		squares = []
		for i in range(9):
			if indexLess:
				squares.append(self.board[i][col])
			else:
				squares.append(((i, col), self.board[i][col]))

	def boxSquares(self, row, col, indexLess = True):
		"""
		Indexed like below
		0 1 2
		3 4 5
		6 7 8

		:param box: index of the wanted box
		:param col: index of col
		:return: list of squares with there indices matching the box above
		"""
		squares = []
		row = box % 3
		col = box // 3
		for i in range(9):
			if indexLess:
				squares.append(self.board[i // 3][i % 3])
			else:
				squares.append(((i // 3, i % 3), self.board[i // 3][i % 3]))
		return squares

	def removeValueFromPossibles(self, rowIndex, colIndex, val):
		"""
		Removes this values as a possible for all sqaure groups associated
		:param row: row index
		:param col: col index
		:param val: value to remove
		"""

		def removeValueFromPossiblesHelper(squareGroup, value):
			"""
			Implements the value removal from a square group
			:param squareGroup: Group of squares to have value removed as possible
			:param value: Value to remove
			"""
			for square in squareGroup:
				square.removePossible(value)

		row = self.rowSquares(rowIndex)
		removeValueFromPossiblesHelper(row, val)

		col = self.colSquares(colIndex)
		removeValueFromPossiblesHelper(col)

		boxIndex = coordinatesToBoxIndex(rowIndex, colIndex)
		box = self.boxSquares(boxIndex)
		removeValueFromPossiblesHelper(box)

	def soleCandidateHelper(self, squareGroup):
		"""
		Implements the sole candidate technique
		:param squareGroup: Either a group of squares from a row, column or box
		"""

		squareGroupValues = [square.getValue() for square in squareGroup]

		# If only a sole value is unset, set it with the missing value
		if squareGroupValues.count(0) == 1:
			soleCandidateIndex = squareGroupValues.index(0)
			soleCandidateValue = (set(squareGroupValues) - set(range(10)))[0]
			soleCandidateSquare = squareGroup[soleCandidateIndex]
			self.setSquare(soleCandidateSquare, soleCandidateValue)

	def soleCandidateFullBoard(self):
		"""
		Runs the Sole Candidate technique on all the rows, columns and boxes of the board
		"""

		for i in range(9):
			row = self.rowSquares(i)
			self.soleCandidateHelper(row)
			col = self.colSquares(i)
			self.soleCandidateHelper(col)
			box = self.colSquares(i)
			self.soleCandidateHelper(box)

	def soleCandidateIndex(self, rowIndex, colIndex):
		"""
		Uses the Sole Candidate technique on one board element
		:param rowIndex: squares row index
		:param colIndex: squares col index
		"""
		row = self.rowSquares(rowIndex)
		self.soleCandidateHelper(row)

		col = self.colSquares(colIndex)
		self.soleCandidateHelper(col)

		boxIndex = coordinatesToBoxIndex(rowIndex, colIndex)
		box = self.colSquares(boxIndex)
		self.soleCandidateHelper(box)

	def uniqueCandidateHelper(self, squareGroup):


	def uniqueCandidateFullBoard(self):
		"""
		Uses the unique candidate technique to set values
		"""

