import sys
from Encoder import *
from Solver import *

def satPlan(argv):
    encoder = Encoder(argv, False)
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
