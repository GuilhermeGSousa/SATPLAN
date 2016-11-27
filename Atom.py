class Atom:
    def __init__(self, ident_template,n_arg):
        self.ident_template = ident_template # template of the atom, e.g., on(x1,x2)
        self.n_arg = n_arg # number of arguments
        




# from string import Template
# s = Template('$who likes $what')
# s.safe_substitute(who='tim', what='kung pao')