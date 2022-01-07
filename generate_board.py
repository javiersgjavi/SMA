import pandas as pd
import numpy as np


def main(path, shape_board, central_point, side):
    array = np.zeros((shape_board, shape_board)).reshape(shape_board, shape_board)
    board = pd.DataFrame(array, dtype=int)
    print(board.shape)
    for i in range(central_point[0] - side // 2, central_point[0] + side // 2):
        for j in range(central_point[1] - side // 2, central_point[1] + side // 2):
            board.iloc[i, j] = 'X'

    board.to_csv(path, index=False, header=False)


if __name__ == '__main__':
    main(path='boards/board_3.txt', shape_board=100, central_point=(50, 50), side=30)
