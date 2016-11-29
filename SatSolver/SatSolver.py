from Cnf import *
import copy




def isEveryClauseTrue(clauses,model):
	for c in clauses:
		list_assigned=[l.name for l in c if l.name in model.var_sol.keys()]
		clauseFalse=True
		for l in list_assigned:
			if model[l.name]==l.signal:
				clauseFalse=False
		if clauseFalse==True:
			return False
	return True

def isAnyClauseFalse(clauses,model):
	for c in clauses:
		for l in c:
			if not l.name in model.var_sol.keys():
				return False
			else:
				clauseFalse=True
				for l in list_assigned:
					if model[l.name]==l.signal:
						clauseFalse=False
				if clauseFalse==True:
					return True
	return False				

def isPureSymbol(clauses,symb):
	for c in clauses:
		pass

def isUnitClause(clauses,symb):
	for c in clauses:
		pass


def solveCNF(clauses,symbols,model=Solution()):

	if isEveryClauseTrue(clauses,model):
		print("All True")
		return True 

	if isAnyClauseFalse(clauses,model):
		print("Any False")
		return False

	for i in range(0,len(symbols)):

		res, val = isPureSymbol(clauses,symbols[i])
		if res:
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model)

		res, val = isUnitClause(clauses,symbols[i])
		if res:
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model)

	symb = symbols.pop()
	rest = symbols

	rest_copy=copy.deepcopy(rest)
	model_copy=copy.deepcopy(model)

	model[symb]=True
	model_copy[symb]=False


	return solveCNF(clauses,rest,model) or solveCNF(clauses,rest_copy,model_copy)

