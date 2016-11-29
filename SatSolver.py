import copy
from Clause import *
#File containing SAT solving functions

def getFromLitList(ident,list_arg): #Get better way to get from model list, use dict?
	for l in list_arg:
		if l.ident==ident:
			return l
	return None

def isEveryClauseTrue(clauses,model):
	#Test if all clauses have at least 1 true literal
	for c in clauses:
		res = c.isClauseTrue(model)
		if res is None:
			return False
		if not res:
			return False
	return True

def isAnyClauseFalse(clauses,model):
	#Test if any clause has all false literals
	for c in clauses:
		if c.isClauseFalse(model):
			return True
	return False

def isUnitClause(clauses, symbol,model):
	
	for c in clauses:
		if c.isClauseTrue(model):
			break
		lit_list = c.getUnassignedLiterals(model)
		if len(lit_list)==1 and lit_list[0].ident==symbol.ident:
			return [True, lit_list[0].signal]
			
	return [False,None]


def isPureSymbol(clauses, symbol):
	isPure=False
	currentSignal=None
	for c in clauses:
		res,lit = c.isInClause(symbol)
		if res:
			if currentSignal==None:
				currentSignal=lit.signal
			elif currentSignal!=lit.signal:
				return [False,None]
	return [True,currentSignal]

def satSolver(clauses,symbols, model=[]): #Will receive a list of clauses, each having a list of grounded literals
										#symbols must be a list of all existing 

	#Find way to return Model if true!

	if isEveryClauseTrue(clauses,model): #REFAZER!!!!!
		print("Every True")
		print(model)
		return True

	if isAnyClauseFalse(clauses,model):  #REFAZER!!!!!
		print("One false")
		print(model)
		return False
			
	for i in range(0,len(symbols)):

		isPure,value_result =isPureSymbol(clauses,symbols[i])

		if isPure:
			print("Pure found")
			print(symbols[i].ident)
			new_literal=symbols.pop(i)
			new_literal.value=value_result
			model.append(new_literal)
			return satSolver(clauses,symbols,model)

		isUnit, value_result = isUnitClause(clauses,symbols[i],model)
		
		if isUnit:
			print("Unit found")
			print(symbols[i].ident)
			new_literal=symbols.pop(i)
			new_literal.value=value_result
			model.append(new_literal)
			return satSolver(clauses,symbols,model)
	print(model)
	print(symbols)
	if not symbols:
		return False

	branch_symbol1 = symbols.pop(0)
	rest=symbols
	branch_symbol2 = copy.deepcopy(branch_symbol1)

	model_copy = copy.deepcopy(model)
	branch_symbol1.value=True
	branch_symbol2.value=False

	model_copy.append(branch_symbol1)
	model.append(branch_symbol2)

	rest_copy = copy.deepcopy(rest)
	return satSolver(clauses,rest_copy, model_copy) or satSolver(clauses,rest, model)

