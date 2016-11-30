from Cnf import *
import copy




def isEveryClauseTrue(clauses,model):
	for c in clauses:
		clauseFalse=True
		for l in c:
			if l.name in model.var_sol.keys():
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
				if model[l.name]==l.signal:
					clauseFalse=False
				if clauseFalse==True:
					return True
	return False				

def isPureSymbol(clauses,symb):
	isPure=False
	currentSignal=None
	for c in clauses:
		for l in c:
			if l.name==symb:
				if currentSignal==None:
					currentSignal=l.signal
				elif currentSignal!=l.signal:
					return [False, None]
	return [True,currentSignal]



def isUnitClause(clauses,symb,model):
	for c in clauses:
		list_unassigned=[l for l in c if l.name not in model.var_sol.keys()]
		if len(list_unassigned)==1 and list_unassigned[0].name==symb:
			return [True , list_unassigned[0].signal]
	return [False, None]


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
			print("isPure")
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model)

		res, val = isUnitClause(clauses,symbols[i],model)
		if res:
			print("isUnit")
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model)


	symb = symbols.pop()
	rest = symbols

	rest_copy=copy.deepcopy(rest)
	model_copy=copy.deepcopy(model)

	model[symb]=True
	model_copy[symb]=False


	return solveCNF(clauses,rest,model) or solveCNF(clauses,rest_copy,model_copy)

