def Cell():
    def __init__(self, position, robot=False, tissue=None):
        self.position = position
        self.robot = robot
        self.tissue = tissue
        self.chem = [0,0,0]

    def get_robot(self):
        return self.robot

    def get_tissue(self):
        return self.tissue

    def set_robot(self, robot):
        self.robot = robot

    def get_chem(self, index):
        return self.chem[index]

    def get_position(self):
        return self.position