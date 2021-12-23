class Cell():
    def __init__(self, position, robot=False, tissue=0):
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

    def get_chemical(self):
        return self.chem

    def get_position(self):
        return self.position

    def print_cell(self):
        res = str(self.tissue)

        if self.robot:
            res = 'X'
        elif self.tissue == 0:
            res =  '▢'
            
        return res