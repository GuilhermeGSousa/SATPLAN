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
		clauseFalse=True
		for l in c:
			if not l.name in model.var_sol.keys():
				return False
			else:
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
		if not any(l.signal==model[l.name] for l in c):
			list_unassigned=[l for l in c if l.name not in model.var_sol.keys()]
			if len(list_unassigned)==1 and list_unassigned[0].name==symb:
				return [True , list_unassigned[0].signal]
	return [False, None]

def learnConflict(clauses,model):
	learned=[]
	for key in model.var_sol.keys():
		tmp=not model[key]
		learned.append(Variable(key,tmp))
	clauses.add(frozenset(learned))
	return clauses


def solveCNF(clauses,symbols,model=Solution(),lvl=0):


	if isEveryClauseTrue(clauses,model):
		print("Solution Found")
		model.success = True
		return (True, model) 

	if isAnyClauseFalse(clauses,model):
		print("Failed, backtracking")
		model.success = False
		clauses=learnConflict(clauses,model)
		return (False, model)

	for i in range(0,len(symbols)):

		res, val = isPureSymbol(clauses,symbols[i])
		if res:
			print(str(symbols[i])+" pure")
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model,lvl+1)

		res, val = isUnitClause(clauses,symbols[i],model)
		if res:
			print(str(symbols[i])+" unit")
			model[symbols.pop(i)]=val
			return solveCNF(clauses,symbols,model,lvl+1)


	rest = copy.deepcopy(symbols)
	symb = rest.pop(0)

	for i in range(0,lvl):
		print("   ",end="")
	print("Branching at "+str(symb))

	rest_copy1=copy.deepcopy(rest)
	model_copy1=copy.deepcopy(model) 
	model_copy2=copy.deepcopy(model)


	model_copy1[symb]=True
	model_copy2[symb]=False


	res1 ,model1 = solveCNF(clauses,rest,model_copy1,lvl+1)
	res2 ,model2 = solveCNF(clauses,rest_copy1,model_copy2,lvl+1)

	if res1:
		model.var_sol=model1.var_sol
		return res1,model1
	if res2:
		model.var_sol=model2.var_sol
		return res2,model2
	else:
		return False,model

