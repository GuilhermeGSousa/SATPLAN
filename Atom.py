class Atom:
    def __init__(self, ident_template,n_arg):
        self.ident_template = ident_template
        self.n_arg = n_arg
        
    def indexAtom(self,t):
        name = self.ident_template + ('_%s'%t)
        self.ident_template = name





# from string import Template
# s = Template('$who likes $what')
# s.safe_substitute(who='tim', what='kung pao')