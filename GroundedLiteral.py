class GroundedLiteral(object):
    """docstring for GroundedLiteral"""

    def __init__(self, ident, signal):
        self.ident = ident # string describing the literal
        self.signal = signal #Negated (False) or not negated (True) 

        self.value = None # true or false


    def indexGL(self,t):
        self.ident += ('_%s'%t)



