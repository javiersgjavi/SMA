from Simulation import Simulation

def main():
    
    path_grid = './boards/l_test_2.txt'
    #path_grid = './boards/grid1.txt'
    fps = 10
    iterations = 500
    colors = {'cell': (255, 255, 255), 'edge': (0, 0, 0), 'robot': (255, 0, 0), 'tissue': (18, 157, 36)}
    alfa = 0.1 # constant of the decay rate
    beta = 0.003 # constant of the injection rate
    gamma = 4 # number of cells of the sum, is the diffusion constant
    initial_charge_chem = 1 # Quantity of the first iteration of injection
    tita = 0.4 # threshold to consider center of chem 1
    p = 0.1 # probability of become a guide robot
    early_stop = True

    simulation = Simulation(
        path_grid=path_grid, 
        iterations=iterations, 
        fps=fps, 
        colors=colors, 
        alfa=alfa, 
        beta=beta, 
        gamma=gamma,
        tita=tita,
        p=p,
        initial_charge_chem=initial_charge_chem,
        early_stop=early_stop
        )

    simulation.run()


if __name__=='__main__':
    main()
