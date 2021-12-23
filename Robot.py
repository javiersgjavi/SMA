from typing_extensions import runtime_checkable
import numpy as np

class Robot():
    
    def __init__(self, position):
        self.movements = [(i,j) for i in range(-1,2) for j in range(-1,2) if not (i==0 and j==0)]
        self.position = position

    def get_position(self):
        return self.position

    def get_neighbours_cells(self, grid):
        neighbours = []

        for movement in self.movements:
            new_position = (self.position[0] + movement[0], self.position[1] + movement[1])

            if grid.is_valid_position(new_position):
                new_cell = grid.get_cell(new_position[0], new_position[1])
                neighbours.append(new_cell)

        return neighbours

    def check_chemical(self, neighbours):
        neighbours_chemical = []
        for neighbour in neighbours:
            if neighbour.get_chemical() != [0,0,0]:
                neighbours_chemical.append(neighbour)

        return neighbours_chemical

    def check_tissue(self, neighbours):
        neighbours_tissue = []
        
        for neighbour in neighbours:
            if neighbour.get_tissue() != 0:
                neighbours_tissue.append(neighbour)

        return neighbours_tissue

    def get_info_neighbours(self, grid):
        neighbours = self.get_neighbours_cells(grid)
        n_tissue = self.check_tissue(neighbours)
        n_chemical = self.check_chemical(neighbours)
        return neighbours, n_tissue, n_chemical


    def random_walk(self, current_cell, neighbours):
        # Select random movement without 
        random_movements = np.random.choice(neighbours, len(neighbours), replace=False)
        
        for new_cell in random_movements:
            if not new_cell.get_robot():
                new_cell.set_robot(True)
                current_cell.set_robot(False)
                self.position = new_cell.get_position()
                break


    def actuate(self, grid):
        current_cell = grid.get_cell(self.position[0], self.position[1])
        neighbours, n_tissue, n_chemical = self.get_info_neighbours(grid)

        if current_cell.get_tissue() != 0:
            # Destroy tissue
            pass

        elif n_tissue:
            #Move to tissue
            pass
        elif n_chemical:
            # Move to chemical
            pass
        else:
            # Random walk
            self.random_walk(current_cell=current_cell, neighbours=neighbours)
            
            

        
