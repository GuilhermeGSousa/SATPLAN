from GroundedLiteral import *
from Action import *
from Atom import *
import copy


def getFunctionNameTerms(f_string):
    i_first = f_string.index("(")
    i_last = f_string.index(")")
    name = f_string[0:i_first]
    terms = f_string[i_first + 1:i_last]
    term = terms.strip(" ").split(',')
    return [name, term]


def templateNameCreator(f_name, terms):
    template_name = f_name + "("
    for i in range(0, len(terms)):
        if i != len(terms) - 1:
            if not terms[i][0].isupper():
                template_name += "$" + terms[i] + "$,"
            else:
                template_name += terms[i] + ","
        else:
            if not terms[i][0].isupper():
                template_name += "$" + terms[i] + "$)"
            else:
                template_name += terms[i] + ")"
    return template_name


def groundedLiteralNameGenerator(f_name, terms):
    name = f_name + "("

    for i in range(0, len(terms)):
        if i != len(terms) - 1:
            name += terms[i] + ","
        else:
            name += terms[i] + ")"
    return name


def generatePossibleSets(nterms, terms):
    set = []
    if nterms == 1:
        for term in terms:
            set.append([term])
        return set
    else:
        subset = generatePossibleSets(nterms - 1, terms)
        for term in terms:
            for i in range(len(subset)):
                set.append([term] + subset[i])
        return set


class Encoder(object):
    """docstring for Encoder"""

    def __init__(self, argv):
        self.init = []  # initial state ground literals
        self.goals = []  # goal state ground literals
        self.sentence =[] # sentence at time t=h
        self.terms_list = []  # constants
        self.clauses = []  # list of grounder clauses
        self.actions = []  # list of actions

        f = open(argv[1], 'r')
        for line in f:
            words = line.strip("\n").split()

            if line[0] == 'I':
                for arg in words[1:]:
                    name, terms = getFunctionNameTerms(arg)

                    # USE name and terms list here
                    for t in terms:
                        if not (t in self.terms_list):
                            self.terms_list.append(t)

                    if name[0] == "-":
                        signal = False
                        name = name[1:]
                    else:
                        signal = True
                    ident = groundedLiteralNameGenerator(name, terms)
                    g_lit = GroundedLiteral(ident, signal)
                    self.init.append(g_lit)

            if line[0] == 'A':
                action_part = line[1:].strip(" ").split(":")[0]
                i_colon = line.index(":")
                i_arrow = line.index(">")
                precond_part = line[i_colon + 1:i_arrow - 1].strip("\n").split(" ")
                effect_part = line[i_arrow + 1:].strip("\n").split(" ")

                action_name, action_terms = getFunctionNameTerms(action_part)
                template_name = templateNameCreator(action_name, action_terms)
                new_action = Action(template_name, action_terms)
                print(template_name)
                # USE ACTION name and terms list here
                for arg in precond_part:
                    if arg != "":
                        precond_name, precond_terms = getFunctionNameTerms(arg)
                        template_name = templateNameCreator(precond_name, precond_terms)
                        new_atom = Atom(template_name, len(precond_terms))
                        new_action.addPreCondition(new_atom)
                        print(template_name)
                for arg in effect_part:
                    if arg != "":
                        effect_name, effect_terms = getFunctionNameTerms(arg)
                        template_name = templateNameCreator(effect_name, effect_terms)
                        new_atom = Atom(template_name, len(effect_terms))
                        new_action.addEffect(new_atom)
                        print(template_name)
                self.actions.append([new_action])

            if line[0] == 'G':
                for arg in words[1:]:
                    name, terms = getFunctionNameTerms(arg)
                    # USE name and terms list here
                    for t in terms:
                        if not (t in self.terms_list):
                            self.terms_list.append(t)

                    if name[0] == "-":
                        signal = False
                        name = name[1:]
                    else:
                        signal = True
                    ident = groundedLiteralNameGenerator(name, terms)
                    g_lit = GroundedLiteral(ident, signal)
                    self.goals.append(g_lit)

    def generateSentence(self, h):
        if h == 0:
            # First, create unit clauses for the initial state
            ninit = len(self.init)
            for i in range(ninit):
                literal=self.init[i]
                name, args = getFunctionNameTerms(literal.ident)
                nargs = len(args)
                print(args)
                combinations = generatePossibleSets(nargs,self.terms_list)
                for comb in combinations:
                    if comb != args:
                        ident=groundedLiteralNameGenerator(name, comb)
                        g_lit = GroundedLiteral(ident,not literal.signal)
                        self.init.append(g_lit)
            for literal in self.init:
                literal.indexGL(0)
                self.clauses.append([literal])

        # Goal is reached in time horizon h
        for literal in self.goals:
            glit = copy.copy(literal) # copy instead of deepcopy because GroundedLiteral doesnt have objects in it
            glit.indexGL(h)
            self.sentence.append([glit])

        print('something')


