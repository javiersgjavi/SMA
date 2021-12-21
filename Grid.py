import numpy as np
from Cell import Cell

def Grid():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))
        self._init_board()

    def _init_board(self):
        for i in range(self.width):
            for j in range(self.height):
                value = self.board[i,j]
                self.board[i][j] = Cell(position=(i,j), tissue=value)


    def get_value(self, i, j):
        return self.board[i, j]

    def set_value(self, i, j, value):
        self.board[i, j] = value

    def get_