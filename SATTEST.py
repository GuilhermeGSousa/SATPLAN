import sys
from GroundedLiteral import *
from Clause import *
from SatSolver import *

def satPlan(argv):
	g1=GroundedLiteral("x1",True)
	g2=GroundedLiteral("x1",False)
	clause1=Clause()
	clause2=Clause()

	clause1.addLiteral(g1)
	clause2.addLiteral(g2)
	res = satSolver([clause1,clause2],[g1])

	print(res)

if __name__ == '__main__':
	satPlan(sys.argv)
