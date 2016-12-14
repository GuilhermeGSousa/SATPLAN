import sys
from Encoder import *
from Solver import *

def satPlan(argv):
    # 1 - Classical ; 2 - Bitwise ; 3 - Bitwise Overloaded Splitting with factoring
    encoder = Encoder(argv, 1)
    t = 0
    while True:
        encoder.generateSentence(t)
        solution = solver()
        SAT = encoder.printSolution(t,solution)
        if SAT:
            break
        t += 1

if __name__ == '__main__':
    satPlan(sys.argv)
