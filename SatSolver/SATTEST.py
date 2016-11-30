import sys
from SatSolver import *
def satPlan(argv):

	cnf=CNF("input.dat")

	sol=solveCNF(cnf.clauses,cnf.symbols)

	print(sol)

if __name__ == '__main__':
	satPlan(sys.argv)
