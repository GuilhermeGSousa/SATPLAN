from Atom import *

class Literal(Atom):
    def __init__(self, ident_template, sign):
        Atom.__init__(self, ident_template)
        self.sign = sign

