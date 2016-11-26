import sys
from Encoder import *

def satPlan(argv):
	encoder = Encoder()
	sentenceSAT = encoder.generateSentence(argv)
    


if __name__ == '__main__':
	satPlan(sys.argv)
