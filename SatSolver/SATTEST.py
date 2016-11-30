import sys
from SatSolver import *
def satPlan(argv):

	cnf=CNF("input.dat")
	s=Solution()
	sol=solveCNF(cnf.clauses,cnf.symbols,s) #Change to return a Solution

	if s.success:
		for i,j in s.var_sol.items():
			print(str(i)+";"+str(j))

if __name__ == '__main__':
	satPlan(sys.argv)
