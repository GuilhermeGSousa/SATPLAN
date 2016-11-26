import sys
from Encoder import *

def satPlan(argv):
	encoder = Encoder(argv)
	sentenceSAT = encoder.generateSentence()
    


if __name__ == '__main__':
	satPlan(sys.argv)
