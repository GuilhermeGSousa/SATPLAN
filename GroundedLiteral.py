import copy

class GroundedLiteral(object):
    """docstring for GroundedLiteral"""

    def __init__(self, ident, signal):
        self.ident = ident # string describing the literal
        self.signal = signal #positive or negative
        self.value = None # true or false

    def __eq__(self, other):
        return (self.ident == other.ident and self.signal == other.signal)

    def __neg__(self):
        new_obj = copy.copy(self)
        new_obj.signal = not self.signal
        return new_obj

    def indexGL(self,t):
        self.ident += ('_%s'%t)
