from Simulation import Simulation

def main():
    
    path_grid = './boards/l_test.txt'
    #path_grid = './boards/grid1.txt'
    fps = 1
    iterations = 20
    colors = {'cell': (255, 255, 255), 'edge': (0, 0, 0), 'robot': (255, 0, 0), 'tissue': (18, 157, 36)}
    beta = 0.1 # constant of the injection rate
    alfa = 0.1 # constant of the decay rate
    simulation = Simulation(path_grid=path_grid, iterations = iterations, fps=fps, colors=colors)
    simulation.run()


if __name__=='__main__':
    main()
