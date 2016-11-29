import sys
from SatSolver import *
def satPlan(argv):
	cnf=CNF("input.dat")

	solveCNF(cnf.clauses,cnf.symbols)

if __name__ == '__main__':
	satPlan(sys.argv)
