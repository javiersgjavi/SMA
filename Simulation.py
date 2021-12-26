import pygame
import time
import sys
from os import environ
import matplotlib.pyplot as plt
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Grid import Grid


class Simulation():

    def __init__(self, path_grid, iterations, colors, block_size=20, fps=1, alfa=0.1, beta=0.1, gamma=1, initial_charge_chem=1, tita=0.1, p=0.1):
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

    def run(self):
        #self.grid.print_board()

        self.drawGrid()
        pygame.display.update()
        self.clock.tick(self.fps)
        for _ in range(self.iterations):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for robot in self.robots:
                robot.actuate(self.grid)

            self.grid.update_chemical_values(self.alfa, self.gamma)

            self.drawGrid()
            pygame.display.update()
            self.clock.tick(self.fps)
        
        history  = self.grid.get_cell(5,5).get_chemical_history()
        x = [h[0] for h in history]
        plt.figure()
        plt.plot(x)
        plt.show()

            
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
        #print(chemical)

        color = list(self.colors['cell'])
        if chemical[0]>0:
            value = 255 - 255 * chemical[0]/self.initial_charge
            color[1] =  50
            color[2] =  50

        elif chemical[1]>0:
            value = 255 - 255 * chemical[1]/self.initial_charge
            color[0] =  50
            color[2] =  50

        elif chemical[2]>0:
            value = 255 - 255 * chemical[2]/self.initial_charge
            color[0] =  50
            color[1] =  50


        rect = pygame.Rect(j_pos, i_pos, self.block_size-2, self.block_size-2)
        
        color = tuple(color)
        pygame.draw.rect(self.screen, color, rect)

    def drawGrid(self):
        self.screen.fill(self.colors['cell'])
        #Set the size of the grid block
        for i in range(0, self.width):
            for j in range(0, self.height):
                rect = pygame.Rect(i*self.block_size, j*self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, self.colors['edge'], rect, 1)

        for i in range(self.width):
            for j in range(self.height):
                cell = self.grid.get_cell(i,j)
                if cell.get_chemical() != [0,0,0]:
                    self.draw_chemical(cell.get_position(), cell.get_chemical())
                if cell.robot:
                    self.draw_robot(cell.get_position())
                elif cell.get_tissue() != 0:
                    self.draw_tissue(cell.get_position())
                   

    
