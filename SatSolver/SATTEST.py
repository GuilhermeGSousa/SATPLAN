import sys
from SatSolver import *
def satPlan(argv):

	cnf=CNF(argv[1])
	s=Solution()

	res, sol=solveCNF(cnf.clauses,cnf.symbols,s) #Change to return a Solution


	print(str(res))
	for i,j in sol.var_sol.items():
		print(str(i)+";"+str(j))



if __name__ == '__main__':
	satPlan(sys.argv)
