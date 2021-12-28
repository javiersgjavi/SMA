import pandas as pd

from Cell import Cell
from Robot import Robot


class Grid():

    def __init__(self, path=None):
        grid = pd.read_csv(path, header=None)
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.board = []
        self.tissue_quantity = 0

        for i in range(self.width):
            row = grid.iloc[i, :].values.tolist()
            self.board.append(row)

    def init_board(self, beta, initial_charge_chem, threshold, p, not_lost):
        robots = []

        for i in range(self.width):
            for j in range(self.height):

                value = self.board[i][j]

                if value == 'X':
                    if not not_lost:
                        lost_limit = None
                        max_distance = None
                    else:
                        lost_limit= not_lost[0]
                        max_distance = not_lost[1]

                    robot = Robot(position=(i, j), beta=beta, charge_chem=initial_charge_chem, threshold=threshold,
                                      p=p, lost_limit=lost_limit, max_distance=max_distance)
                    robots.append(robot)
                    cell = Cell(position=(i, j), robot=True)

                else:
                    value = int(value)
                    cell = Cell(position=(i, j), tissue=int(value))

                    if value > 0:
                        self.tissue_quantity += value

                self.board[i][j] = cell

        return robots

    def get_tissue_amount(self):
        return self.tissue_quantity

    def get_cell(self, i, j):
        return self.board[i][j]

    def get_shape(self):
        return self.width, self.height

    def is_valid_position(self, position):
        if position[0] < 0 or position[0] >= self.width:
            return False
        if position[1] < 0 or position[1] >= self.height:
            return False
        return True

    def _get_neighbours_cells(self, position, gamma):
        neighbours = []
        for i in range(position[0] - gamma // 2, position[0] + gamma // 2 + 1):
            for j in range(position[1] - gamma // 2, position[1] + gamma // 2 + 1):
                if self.is_valid_position((i, j)) and (i, j) != position:
                    neighbours.append(self.board[i][j])
        return neighbours

    def calculate_new_chemical_value(self, cell, alfa, gamma, chem):
        neighbours = self._get_neighbours_cells(cell.get_position(), gamma)
        n_chem_value = sum(n.get_chemical()[chem] for n in neighbours)
        current_value = cell.get_chemical()[chem]
        injection_value = cell.get_injected_chemical()[chem]

        #         summatory                              decay                injection
        value = (1 / (gamma ** 4)) * n_chem_value - (alfa * current_value) + injection_value
        value = 0 if value < 0 else value
        cell.set_next_chemical(chem + 1, value)

    def update_chemical_values(self, alfa, gamma):
        set_to_update = set()
        for i in range(self.width):
            for j in range(self.height):
                cells_to_update = []
                cell = self.board[i][j]
                injected, chem = cell.get_has_been_injected()
                if injected:
                    cells_to_update = self._get_neighbours_cells(cell.get_position(), gamma)
                    self.calculate_new_chemical_value(cell, alfa, gamma, chem)
                    for n in cells_to_update:
                        self.calculate_new_chemical_value(n, alfa, gamma, chem)

                set_to_update.add(cell)
                set_to_update.update(cells_to_update)

        for c in set_to_update:
            c.update_chemical()

    def print_board(self):
        msg = ''
        for i in range(self.width):
            row = self.board[i]
            for j in range(self.height):
                cell = row[j].print_cell()
                msg += cell
            msg += '\n'

        print(msg)
