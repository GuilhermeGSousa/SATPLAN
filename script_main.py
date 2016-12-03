from Encoder import *

# para poder fazer debugg, preciso de ter a main como script acho eu

argv = ['lixo','input.dat']

my_e = Encoder(argv,False)

my_e.generateSentence(0)
my_e.generateSentence(1)
my_e.generateSentence(2)

my_e.printSolution(2)