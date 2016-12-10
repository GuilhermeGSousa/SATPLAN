import sys
from IterativeSatSolver import *


def satPlan():

	cnf=CNF("dimacs.dat")
	s=Solution()
	solutionList=[]
	print(len(cnf.clauses))
	res, sol=solveIterativeCNF(cnf.clauses,cnf.symbols,s) #Change to return a Solution

	
	if res:
		solutionList[0]='SAT'
		for key,val in sol.var_sol.items():
			if val:
				solutionList.append(key)
			else:
				solutionList.append(-1*key)
	else:
		solutionList[0]='UNSAT'

	return solutionList