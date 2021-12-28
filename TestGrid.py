from objects.Simulation import Simulation


def main():
    path_grid = 'boards/board_3.txt'
    fps = 15
    block_size = 10
    iterations = 500
    colors = {'cell': (255, 255, 255), 'edge': (0, 0, 0), 'robot': (255, 0, 0), 'tissue': (18, 157, 36),
              'exit': (155, 0, 255), 'chem1': (255, 50, 50), 'chem2': (50, 255, 50), 'chem3': (50, 50, 255)}
    alfa = 0.1  # constant of the decay rate
    beta = 0.003  # constant of the injection rate
    gamma = 7  # number of cells of the sum, is the diffusion constant
    initial_charge_chem = 1  # Quantity of the first iteration of injection
    tita = 0.2  # threshold to consider center of chem 1
    p = 0.1  # probability of become a guide robot
    early_stop = True
    return_position = iterations // 2
    not_lost = (90, 5)  # use to ensure robots are not lost, to no use it, set to None
    not_lost = None

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
        early_stop=early_stop,
        return_position=return_position,
        not_lost=not_lost,
        block_size=block_size
    )

    simulation.run()


if __name__ == '__main__':
    main()
