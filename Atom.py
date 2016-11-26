
class Atom:
    def __init__(self, ident_template,):
        self.ident_template = ident_template

    def indexAtom(self,t):
        name = self.ident_template + ('_%s'%t)
        self.ident_template = name





# from string import Template
# s = Template('$who likes $what')
# s.safe_substitute(who='tim', what='kung pao')