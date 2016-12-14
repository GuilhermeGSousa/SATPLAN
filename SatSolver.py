from Cnf import *
import copy


def isClauseActive(clause, model): #Make function to test is the clause is not yet assigned
	return not any(l.name in model.var_sol.keys() and l.signal==model[l.name] for l in clause)

def isEveryClauseTrue(clauses,model):# Given a model, tests if every clause is true
	for c in clauses:
		clauseFalse=True
		for l in c:
			if l.name in model.var_sol.keys():
				if model[l.name]==l.signal:
					clauseFalse=False
		if clauseFalse==True:
			return False
	return True

def isAnyClauseFalse(clauses,model):#For a given model, finds any false clause
	for c in clauses:
		clauseFalse=True
		for l in c:
			if not l.name in model.var_sol.keys():
				clauseFalse=False
			else:
				if model[l.name]==l.signal:
					clauseFalse=False
		if clauseFalse==True:
			return [True,c]
	return [False, None]				

def isPureSymbol(clauses,symb,model):#checks if a symbol is pure
	currentSignal=None
	for c in clauses:
		if isClauseActive(c,model):
			for l in c:
				if l.name==symb:
					if currentSignal==None:
						currentSignal=l.signal
					elif currentSignal!=l.signal:
						return [False, None]
	if currentSignal == None:
		return[False,None]
	else:
		return[True,currentSignal]



def isUnitClause(clauses,symb,model):#checks if a simbol is the last unassigned variable in a clause
	for c in clauses:
		if isClauseActive(s,model):
			list_unassigned=[l for l in c if l.name not in model.var_sol.keys()]
			if len(list_unassigned)==1 and list_unassigned[0].name==symb:
				return [True , list_unassigned[0].signal]
	return [False, None]

def assignUnitSymbols(clauses,symbols,model):#Puts all unit symbols in the model
	changes=[]
	for c in clauses:
		if isClauseActive(c,model):
			list_unassigned=[l for l in c if l.name not in model.var_sol.keys()]
			if len(list_unassigned)==1:
				symbols.remove(list_unassigned[0].name)
				model[list_unassigned[0].name]=list_unassigned[0].signal
				changes.append(list_unassigned[0].name)

	return changes
	
