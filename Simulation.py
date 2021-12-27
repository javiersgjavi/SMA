import pygame
import time
import sys
from os import environ
import matplotlib.pyplot as plt
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Grid import Grid


class Simulation():

    def __init__(self, path_grid, iterations, colors, block_size=20, fps=1, alfa=0.1, beta=0.1, gamma=1, initial_charge_chem=1, tita=0.1, p=0.1, early_stop=False):
        self.alfa = alfa
        self.gamma = gamma
        self.colors = colors
        self.fps = fps
        self.initial_charge=initial_charge_chem
        self.grid = Grid(path=path_grid)
        self.robots = self.grid.init_board(beta=beta, initial_charge_chem=self.initial_charge, threshold=tita, p=p)
        self.iterations = iterations
        self.width, self.height = self.grid.get_shape()
        self.block_size = block_size
        self.screen = pygame.display.set_mode((self.height*self.block_size, self.height*self.block_size))
        self.clock = pygame.time.Clock()
        self.screen.fill(self.colors['cell'])
        self.early_stop = early_stop

    def run(self):
        tissue_amount = [self.grid.get_tissue_amount()]

        self.drawGrid(tissue_amount)
        pygame.display.update()
        self.clock.tick(self.fps)
        for _ in range(self.iterations):
            print("\n Iteration: ", _, '--------'*10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for robot in self.robots:
                robot.actuate(self.grid)

            self.grid.update_chemical_values(self.alfa, self.gamma)

            tissue_amount = self.drawGrid(tissue_amount)
            pygame.display.update()
            self.clock.tick(self.fps)

            if self.early_stop and tissue_amount[-1] == 0:
                break

        self.print_tissue_decay(tissue_amount)
        

            
    def draw_robot(self, position):
        i_pos = (position[0]*self.block_size)+(self.block_size/2)
        j_pos = (position[1]*self.block_size)+(self.block_size/2)
        new_position = (j_pos, i_pos)
        pygame.draw.circle(self.screen, self.colors['edge'], new_position, 5)

    def draw_tissue(self, position):
        i_pos = (position[0]*self.block_size)+(self.block_size/4)
        j_pos = (position[1]*self.block_size)+(self.block_size/4)

        rect = pygame.Rect(j_pos, i_pos, self.block_size/2, self.block_size/2)

        pygame.draw.rect(self.screen, self.colors['tissue'], rect)

    def draw_chemical(self, position, chemical):
        i_pos = (position[0]*self.block_size)+(self.block_size) + 1
        j_pos = (position[1]*self.block_size)+(self.block_size) + 1

        color = list(self.colors['cell'])
        if chemical[0]>0:
            color[1] =  50
            color[2] =  50

        elif chemical[1]>0:
            color[0] =  50
            color[2] =  50

        elif chemical[2]>0:
            color[0] =  50
            color[1] =  50


        rect = pygame.Rect(j_pos, i_pos, self.block_size-2, self.block_size-2)
        
        color = tuple(color)
        pygame.draw.rect(self.screen, color, rect)

    def drawGrid(self, tissue_amount):
        self.screen.fill(self.colors['cell'])

        #Set the size of the grid block
        for i in range(0, self.width):
            for j in range(0, self.height):
                rect = pygame.Rect(i*self.block_size, j*self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, self.colors['edge'], rect, 1)

        tissue = 0
        for i in range(self.width):
            for j in range(self.height):
                cell = self.grid.get_cell(i,j)
                tissue += cell.get_tissue()
                if cell.get_chemical() != [0,0,0]:
                    self.draw_chemical(cell.get_position(), cell.get_chemical())
                if cell.robot:
                    self.draw_robot(cell.get_position())
                elif cell.get_tissue() != 0:
                    self.draw_tissue(cell.get_position())

        tissue_amount.append(tissue)

        return tissue_amount

    def print_tissue_decay(self, serie):
        plt.figure(figsize=(10,5))
        plt.title('Tissue decay')
        plt.xlabel('Iterations')
        plt.ylabel('Tissue amount')
        plt.plot(serie)
        plt.axis([0, None, 0, None])
        plt.show()
                   

    
