
class Action():
    def __init__(self, name_template,args):
        self.name_template = name_template
        self.args = args
        self.efx = [] # lists of Atoms
        self.preconds =[]

    def addPreCondition(self, atom):
        self.preconds.append(atom)

    def addEffect(self,atom):
        self.efx.append(atom)



