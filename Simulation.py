from Grid import Grid

class Simulation():

    def __init__(self, path_grid, iterations):
        self.grid = Grid(path=path_grid)
        self.robots = self.grid.init_board()
        self.iterations = iterations

    def run(self):
        self.grid.print_board()
        for _ in range(self.iterations):
            for robot in self.robots:
                robot.actuate(self.grid)

            self.grid.print_board()
            print('---')