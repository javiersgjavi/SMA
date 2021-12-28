from typing_extensions import runtime_checkable
import numpy as np
import itertools


class Robot():
    new_id = itertools.count()

    def __init__(self, position, beta, charge_chem, threshold, p):
        self.id = next(self.new_id)
        self.movements = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
        self.position = position
        self.original_position = self.position
        self.beta = beta
        self.charge_chem = charge_chem
        self.threshold = threshold
        self.p = p
        self.injection_value = None
        self.is_guide = False
        self.injected = []
        self.threshold = 0.5

    def get_id(self):
        return self.id

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
            if neighbour.get_chemical() != [0, 0, 0]:
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

    def liberate_chemical(self, cell, chem):
        cell.inject_chemical(chem, self.injection_value)
        print(f'Robot {self.get_id()} liberating chemical {chem} in cell {cell.get_position()}')
        self.injection_value -= self.beta * self.injection_value
        if round(self.injection_value, 4) == 0:
            self.is_guide = False
            self.injection_value = None

    def set_guide_robot(self, current_cell, chem):
        print(f'Robot {self.get_id()} is now guiding chemical {chem}')
        self.is_guide = True
        self.injected.append(chem)
        self.injection_value = self.charge_chem
        self.liberate_chemical(current_cell, self.injected[-1])

    def get_chemical_decision(self, current_cell, n_chemical):
        next_moment = current_cell
        chem_pos = None
        current_chemical = current_cell.get_chemical()
        for i in n_chemical:
            i_chem = i.get_chemical()

            if i_chem[0] >= current_chemical[0] and i_chem[0] != 0 and not i.get_robot():
                next_moment = i
                chem_pos = 0

            elif i_chem[1] >= current_chemical[1] and i_chem[1] != 0 and not i.get_robot():
                next_moment = i
                chem_pos = 1

            elif i_chem[2] >= current_chemical[2] and not i.get_robot():
                next_moment = i
                chem_pos = 2

        if next_moment != current_cell:
            guide = np.random.uniform(0, 1)
            if chem_pos != 2:
                if (current_chemical[chem_pos + 1] == 0) and (chem_pos + 1 not in self.injected) and guide < self.p:
                    self.set_guide_robot(current_cell, chem_pos + 2)

            self.random_walk(current_cell=current_cell, neighbours=[next_moment])

    def actuate(self, grid):

        current_cell = grid.get_cell(self.position[0], self.position[1])
        neighbours, n_tissue, n_chemical = self.get_info_neighbours(grid)

        # If the it is a guide robot, continue injecting chemical
        if self.is_guide:
            print(f'Robot {self.get_id()} is guide')
            self.liberate_chemical(current_cell, self.injected[-1])

        elif current_cell.get_tissue() != 0:
            print(f'Robot {self.get_id()} attack tissue')
            current_cell.attack_tissue()

            # Liberate chem
            if current_cell.get_chemical()[0] == 0 and (1 not in self.injected):
                print(f'Robot {self.get_id()} starts to inject chemical 1')
                self.set_guide_robot(current_cell, 1)

        elif n_tissue:
            print(f'Robot {self.get_id()} goes to tissue')
            self.random_walk(current_cell=current_cell, neighbours=n_tissue)

        elif n_chemical and not (current_cell.get_chemical()[0] > self.threshold):
            self.get_chemical_decision(current_cell, n_chemical)
        else:
            # Random walk
            self.random_walk(current_cell=current_cell, neighbours=neighbours)

    def get_distance_origin(self, candidate_cell):
        return np.sqrt(
            (self.original_position[0] - candidate_cell.get_position()[0]) ** 2 +
            (self.original_position[1] - candidate_cell.get_position()[1]) ** 2)

    def exit(self, grid):
        current_cell = grid.get_cell(self.position[0], self.position[1])
        neighbours, _, _ = self.get_info_neighbours(grid)

        if self.original_position != self.position:
            error_probability = np.random.uniform(0, 1)
            if error_probability < 0.3:
                self.random_walk(current_cell=current_cell, neighbours=neighbours)
            else:
                position_by_distance = {self.get_distance_origin(n): i for i, n in
                                        enumerate(neighbours)}
                #print(position_by_distance, self.position)
                for i_distance in np.sort(list(position_by_distance.keys())):
                    target_cell = neighbours[position_by_distance[i_distance]]
                    if not target_cell.get_robot():
                        #print(target_cell.get_position())
                        self.random_walk(current_cell=current_cell, neighbours=[target_cell])
                        break
