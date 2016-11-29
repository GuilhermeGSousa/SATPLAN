class Atom:
    def __init__(self, ident_template,n_arg):
        self.ident_template = ident_template # template of the atom, e.g., on(x1,x2)
        self.n_arg = n_arg # number of arguments

    def checkSign(self,name):
        if name[0] == "-":
            return [False, name[1:]]
        else:
            return [True, name]