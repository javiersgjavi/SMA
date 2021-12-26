class Cell():
    def __init__(self, position, robot=False, tissue=0):
        self.position = position
        self.robot = robot
        self.tissue = tissue
        self.has_been_injected = (False, None)
        self.chem = [0,0,0] # chemical values in moment t
        self.next_chem = [0,0,0] # chemical values in moment t+1
        self.injected_chem = [0,0,0] # injected chemical values in moment t
        self.chem_history = [] # history of chemical values in moment t

    def get_robot(self):
        return self.robot

    def get_tissue(self):
        return self.tissue

    def attack_tissue(self):
        self.tissue -= 1

    def set_robot(self, robot):
        self.robot = robot

    def get_next_chemical(self):
        return self.next_chem

    def set_next_chemical(self, chem, value):
        self.next_chem[chem-1] = value

    def get_chemical(self):
        return self.chem

    def set_chemical(self, chem, value):
        self.chem[chem-1] += value

    def get_chemical_history(self):
        return self.chem_history

    def update_chemical(self):
        
        if self.position == (5,5):
            #print(f'{self.chem} <--- {self.next_chem}')
            pass

        self.chem_history.append(self.chem)
        self.chem = self.next_chem
        self.next_chem =  [0,0,0] # De aqui puede estar viniendo un error bastante gordo RECALCO ESTO
        self.injected_chem = [0,0,0]
        
        
    def get_has_been_injected(self):
        return self.has_been_injected
        
    def inject_chemical(self, chem, value):
        self.has_been_injected = (True, chem-1)
        self.injected_chem[chem-1] = value

    def get_injected_chemical(self):
        return self.injected_chem

    def get_position(self):
        return self.position

    def print_cell(self):
        res = str(self.tissue)

        if self.robot:
            res = 'X'
        elif self.tissue == 0:
            res =  '▢'
            
        return res