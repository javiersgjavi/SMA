import numpy as np
import pandas as pd
from Cell import Cell
from Robot import Robot

class Grid():

    def __init__(self, path=None):
        grid = pd.read_csv(path, header=None)
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.board = []

        for i in range(self.width):
            row = grid.iloc[i,:].values.tolist()
            self.board.append(row)
        
    def init_board(self):
        robots = []

        for i in range(self.width):
            for j in range(self.height):

                value = self.board[i][j]

                if value == 'X':
                    robot = Robot(position=(i, j))
                    robots.append(robot)
                    cell = Cell(position=(i, j), robot=True)

                else:
                    cell = Cell(position=(i,j), tissue=int(value))

                self.board[i][j] = cell

        return robots

    def get_cell(self, i, j):
        return self.board[i][j]

    def get_shape(self):
        return (self.width, self.height)

    def is_valid_position(self, position):
        if position[0] < 0 or position[0] >= self.width:
            return False
        if position[1] < 0 or position[1] >= self.height:
            return False
        return True


    def print_board(self):
        msg = ''
        for i in range(self.width):
            row = self.board[i]
            for j in range(self.height):
                cell = row[j].print_cell()
                msg += cell
            msg+='\n'

        print(msg)

