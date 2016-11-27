from GroundedLiteral import *

class Clause:

    def __init__(self):
        self.literals = []


    def addLiteral(self, literal):
        self.literals.append(literal)

    def getUnassignedLiterals(self,model):
    	lit_list=[]

    	for l in self.literals:
    		if not any(m.ident==l.ident for m in model):
    			lit_list.append(l)

    	return lit_list

    def isInClause(self,symbol):
    	for l in self.literals:
    		if l.ident==symbol.ident:
    			return [True, l]
    	return [False, None]



