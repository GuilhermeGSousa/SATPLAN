import sys

from IterativeSatSolver import *
def satPlan(argv):

	print("Reading file")
	cnf=CNF(argv[1])
	s=Solution()
	print("Starting solver")
	start_time=time.time()
	
	
	print(len(cnf.clauses))
	res, sol=solveIterativeCNF(cnf.clauses,cnf.symbols,s) #Change to return a Solution

	print("Running time: %s seconds" % (time.time() - start_time))
	print("Is solvable: "+str(res))
	if res:
		print("Solution:")
		for i,j in sol.var_sol.items():
			print(str(i)+";"+str(j))

if __name__ == '__main__':
	satPlan(sys.argv)
