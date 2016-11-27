import copy

#File containing SAT solving functions

def getClauseStatus(clause):
	existsUnassigned=False
	for l in clause.literals:
		if (l.signal and l.value==True) or ((not l.signal) and (l.value==False)): #l.value can be = to None
				return True
		if l.value==None and not existsUnassigned:
			existsUnassigned=True
	if existsUnassigned:
		return None
	else:
		return False
from Clause import *

def isEveryClauseTrue(clauses):
	for c in clauses:
		if getClauseStatus(c)==False or getClauseStatus(c)==None:
			return False
	return True

def isAnyClauseFalse(clauses):
	for c in clauses:
		if getClauseStatus(c)==False:
			return True
	return False

def isUnitClause(clauses, symbol,model):
	
	for c in clauses:
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
	if isEveryClauseTrue(clauses):
		return True

	if isAnyClauseFalse(clauses):
		return False
			
	for i in range(0,len(symbols)):

		isPure,value_result =isPureSymbol(clauses,symbols[i])

		if isPure:
			new_literal=symbols.pop(i)
			new_literal.value=value_result
			model.append(new_literal)
			return satSolver(clauses,symbols,model)

		isUnit, value_result = isUnitClause(clauses,symbols[i],model)
		
		if isUnit:
			new_literal=symbols.pop(i)
			new_literal.value=value_result
			model.append(new_literal)
			return satSolver(clauses,symbols,model)

	if not symbols: #Empty list
		return False
	else:
		branch_symbol1 = symbols.pop(0)
		rest=symbols
		branch_symbol2 = copy.deepcopy(branch_symbol1)

		branch_symbol1.value=True
		branch_symbol2.value=False
		return satSolver(clauses,rest, model.append(branch_symbol1)) or satSolver(clauses,rest, model.append(branch_symbol2))

