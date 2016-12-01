from GroundedLiteral import *
from Action import *
from Atom import *
import copy
import string
import time


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
                template_name += "$" + terms[i] + ","  # + "$,"
            else:
                template_name += terms[i] + ","
        else:
            if not terms[i][0].isupper():
                template_name += "$" + terms[i] + ")"  # + "$)"
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


def mapAndSubstitute(comb, args, temp):
    mapping = {}
    for i, arg in enumerate(args):
        mapping[arg] = comb[i]
    ident = string.Template(temp)
    name = ident.safe_substitute(mapping)
    return name


class Encoder(object):
    """docstring for Encoder"""

    def __init__(self, argv):
        self.init = []  # initial state ground literals
        self.goals = []  # goal state ground literals
        self.sentence = []  # sentence at time t=h
        self.terms_list = []  # constants
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
                self.actions.append(new_action)

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

    def createIndexedActionLiteral(self, comb, action, sign, t):
        name = mapAndSubstitute(comb, action.args, action.name_template)
        action_glit = GroundedLiteral(name, sign)
        action_glit.indexGL(t)
        return action_glit

    def initialStateClauses(self):
        ninit = len(self.init)
        for i in range(ninit):
            literal = self.init[i]
            name, args = getFunctionNameTerms(literal.ident)
            nargs = len(args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                flag = False
                if comb != args:
                    ident = groundedLiteralNameGenerator(name, comb)
                    for glit in self.init:
                        if ident == glit.ident:
                            flag = True
                            break
                    if flag:
                        continue
                    else:
                        g_lit = GroundedLiteral(ident, not literal.signal)
                        self.init.append(g_lit)
        for literal in self.init:
            literal.indexGL(0)
            self.sentence.append([literal])

    def actionsImplications(self, t):
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                aglit = self.createIndexedActionLiteral(comb, action, False, t)
                for effect in action.efx:
                    name = mapAndSubstitute(comb, action.args, effect.ident_template)
                    sign, name = effect.checkSign(name)
                    effect_glit = GroundedLiteral(name, sign)
                    effect_glit.indexGL(t + 1)
                    self.sentence.append([aglit, effect_glit])
                for precond in action.preconds:
                    name = mapAndSubstitute(comb, action.args, precond.ident_template)
                    sign, name = precond.checkSign(name)
                    precond_glit = GroundedLiteral(name, sign)
                    precond_glit.indexGL(t)
                    self.sentence.append([aglit, precond_glit])

    def propagateSteadyStates(self, t):
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                aglit = self.createIndexedActionLiteral(comb, action, False, t)
                modified = {}
                for effect in action.efx:
                    name = mapAndSubstitute(comb, action.args, effect.ident_template)
                    name = effect.checkSign(name)[1]
                    atom_name, terms = getFunctionNameTerms(name)
                    if atom_name in modified.keys():
                        modified[atom_name].append(terms)
                    else:
                        modified[atom_name] = [terms]
                for atom_name, list_terms in modified.items():
                    nargs = len(list_terms[0])
                    subset = generatePossibleSets(nargs, self.terms_list)
                    for comb2 in subset:
                        if comb2 not in list_terms:
                            name = groundedLiteralNameGenerator(atom_name, comb2)
                            glit1 = GroundedLiteral(name, False)
                            glit2 = GroundedLiteral(name, True)
                            glit1.indexGL(t)
                            glit2.indexGL(t + 1)
                            self.sentence.append([aglit, glit1, glit2])

    def oneActionPerTimeStep(self, t):
        at_least_one = []
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                aglit = self.createIndexedActionLiteral(comb, action, True, t)
                at_least_one.append(aglit)
        self.sentence.append(at_least_one)

        # At most one action per time step
        alist = []
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                a = self.createIndexedActionLiteral(comb, action, False, t)
                alist.append(a)
        for i, a1 in enumerate(alist):
            for j, a2 in enumerate(alist):
                if j > i:
                    self.sentence.append([a2, a1])

    def addGoalStates(self, t):
        for literal in self.goals:
            glit = copy.copy(literal)  # copy instead of deepcopy because GroundedLiteral doesnt have objects in it
            glit.indexGL(t + 1)
            self.sentence.append([glit])

    def removePreviousGoalStates(self):
        nlits = len(self.goals)
        del (self.sentence[-nlits:])

    def translateDIMACS(self):
        pass

    def generateSentence(self, t):
        time1=time.time()
        # First, create unit clauses for the initial state
        if t == 0:
            self.initialStateClauses()
        else:
            self.removePreviousGoalStates()

        # Actions imply their preconditions and effects
        self.actionsImplications(t)

        # Atoms not modified by an action are propagated in time
        self.propagateSteadyStates(t)

        # At least ne action per time step
        self.oneActionPerTimeStep(t)

        # Goal is reached in time horizon h
        self.addGoalStates(t)

        lits = [c[l] for c in self.sentence for l in c]

        numbers_dict = {}

        for lit in lits:
            if lit.ident not in numbers_dict.keys():
                numbers_dict[lit.ident] = len(numbers_dict)+1

        for clause in self.sentence:
            





        print(time.time()-time1)
        print('something')
