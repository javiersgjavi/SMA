import numpy as np

def Robot():
    self.movements = [(i,j) for i in range(-1,2) for j in range(-1,2)]

    def __init__(self, position):
        self.position = position

    def random_walk(self):
        actions_tried = []


        action = np.random.randint(len(self.movements))
        new_position = (self.position[0] + self.movements[action][0], self.position[1] + self.movements[action][1])
        # check position is a valid position

    def get_behaviour(self):
        '''Se debe implementar en cada robot'''
        pass