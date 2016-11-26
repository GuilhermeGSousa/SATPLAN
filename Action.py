from Atom import *


class Action(Atom):
    def __init__(self, name_template):
        Atom.__init__(self, name_template)
        self.efx = [] # lists of Atoms
        self.precond =[]

    def addPreCondition(self, literal):
        self.precond.append([literal])

    def addEffect(self,literal):
        self.efx.append([literal])



