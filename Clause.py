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

	def isClauseTrue(self,model):

		if model is not None:
			for m in model:
				res,val = self.isInClause(m)
				if res is True:
					if m.value==val.signal:
						return True
		return False

	def isClauseFalse(self,model):

		if model is not None:
			false_count = 0
			for m in model:
				res,val = self.isInClause(m)
				if res is True:
					if m.value!=val.signal:
						false_count+=1

			if false_count== len(self.literals):
				return True
		return False



