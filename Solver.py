import sys
from IterativeSatSolver import *


def solver():

	cnf=CNF('dimacs.dat')
	s=Solution(var_sol={})
	solutionList=[]
	res, sol=solveIterativeCNF(cnf.clauses,cnf.symbols,s)
	if res:
		solutionList.append('SAT')
		for key,val in sol.var_sol.items():
			if val:
				solutionList.append(key)
			else:
				solutionList.append(-1*key)
	else:
		solutionList.append('UNSAT')

	return solutionList