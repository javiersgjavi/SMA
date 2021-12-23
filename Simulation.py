import pygame
import time
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from Grid import Grid


class Simulation():

    def __init__(self, path_grid, iterations, colors, block_size=20, fps=1):
        self.colors = colors
        self.fps = fps
        self.grid = Grid(path=path_grid)
        self.robots = self.grid.init_board()
        self.iterations = iterations
        self.width, self.height = self.grid.get_shape()
        self.block_size = block_size
        self.screen = pygame.display.set_mode((self.height*self.block_size, self.height*self.block_size))
        self.clock = pygame.time.Clock()
        self.screen.fill(self.colors['cell'])

    def run(self):
        #self.grid.print_board()
        self.drawGrid()
        for _ in range(self.iterations):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for robot in self.robots:
                robot.actuate(self.grid)

            self.drawGrid()
            pygame.display.update()
            self.clock.tick(self.fps)
            
    def draw_robot(self, position):
        i_pos = (position[0]*self.block_size)+(self.block_size/2)
        j_pos = (position[1]*self.block_size)+(self.block_size/2)
        new_position = (j_pos, i_pos)
        pygame.draw.circle(self.screen, self.colors['robot'], new_position, 5)

    def draw_tissue(self, position):
        i_pos = (position[0]*self.block_size)+(self.block_size/4)
        j_pos = (position[1]*self.block_size)+(self.block_size/4)

        rect = pygame.Rect(j_pos, i_pos, self.block_size/2, self.block_size/2)

        pygame.draw.rect(self.screen, self.colors['tissue'], rect)

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
                if cell.robot:
                    self.draw_robot(cell.get_position())
                elif cell.get_tissue() != 0:
                    self.draw_tissue(cell.get_position())
                   

    
