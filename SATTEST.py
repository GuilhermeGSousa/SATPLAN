import sys
from GroundedLiteral import *
from Clause import *
from SatSolver import *

def satPlan(argv):
	g1=GroundedLiteral("x1",True)
	g2=GroundedLiteral("x2",False)
	g3=GroundedLiteral("x2",True)

	clause1=Clause()
	clause2=Clause()

	clause1.addLiteral(g1)
	clause1.addLiteral(g2)
	clause2.addLiteral(g3)
	
	res = satSolver([clause1,clause2],[g1,g3])

	print(res)

if __name__ == '__main__':
	satPlan(sys.argv)
