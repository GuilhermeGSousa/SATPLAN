from SatSolver import *

def decideBranch(branched,symbols,model):

	if symbols is not None and len(symbols)>0:

		for s in symbols:

			if branched.keys() is None:
				val=s
				symbols.remove(s)
				model[val]=False
				branched[val]=False
				return [val,False]


			if s not in branched.keys():
				val=s
				symbols.remove(s)
				model[val]=False
				branched[val]=False
				return [val,False]


			if branched[s]==False:
				val=s
				symbols.remove(s)
				model[val]=True
				branched[val]=True
				return [val,True]

	return [None, False]

def deduceStatus(clauses,symbols,model):
	changes=[]



	if isEveryClauseTrue(clauses,model):
		model.success = True
		print("all true")
		return ["SAT",changes]

	res,clause =isAnyClauseFalse(clauses,model)
	if res:
		model.success = False
		#clauses=learnConflict(clauses,model)  #Clause learning (not improving run times)
		return ["CONFLICT",changes]

	if symbols is not None:
		for s in symbols:
			res, val = isPureSymbol(clauses,s)
			if res:
				symbols.remove(s)
				model[s]=val
				changes.append(s)
				continue

			res, val = isUnitClause(clauses,s,model)
			if res:
				symbols.remove(s)
				model[s]=val
				changes.append(s)
				continue


	return["OTHER",changes]


def analyzeConflict(clauses,model,lvl):
	#learnConflict(clauses,model)
	return lvl-1

def backtrackToLevel(changed,symbols,model,blvl,lvl):


	for i in range(blvl,lvl+1):
		if i>0:
			for s in changed[i]:
				if s in model.var_sol.keys():
					symbols.append(s)
					del model.var_sol[s]

def solveIterativeCNF(clauses,symbols,model=Solution()):
	branched={}
	changed={}
	lvl=0
	while True:

		symb,val=decideBranch(branched,symbols,model)  #Implement heuristic here

		if symb is not None:
			for i in range(0,lvl):
				print(" ",end="")
			print("Branching: "+str(symb))
			lvl=lvl+1
			changed[lvl]=[symb]
		while True:
			status, changes= deduceStatus(clauses,symbols,model)
			if lvl>0:
				changed[lvl].extend(changes)

			if status == "CONFLICT":
				blvl=analyzeConflict(clauses,model,lvl)
				if lvl==0:
					return [False, model]
				backtrackToLevel(changed,symbols,model,blvl,lvl)
				lvl=blvl
			elif status == "SAT":
				return [True, model]
			else:
				break