from Simulation import Simulation

def main():
    
    path_grid = './boards/l_test.txt'
    iterations = 5
    simulation = Simulation(path_grid=path_grid, iterations = iterations)
    simulation.run()


if __name__=='__main__':
    main()
