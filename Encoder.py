from GroundedLiteral import *
from Action import *
from Atom import *
import string
import time
import math


def getFunctionNameTerms(f_string):
    # This function gets a string that includes
    # the function name with its arguments
    # and returns them separated
    i_first = f_string.index("(")
    i_last = f_string.index(")")
    name = f_string[0:i_first]
    terms = f_string[i_first + 1:i_last]
    term = terms.strip(" ").split(',')
    return [name, term]


def templateNameCreator(f_name, terms):
    # This function receives the function name and
    # its terms and rewrites its name in the format
    #             'function($arg1,$arg2)'
    # in order to use the method from the string object
    # further ahead
    template_name = f_name + "("
    for i in range(0, len(terms)):
        if i != len(terms) - 1:
            if not terms[i][0].isupper():
                template_name += "$" + terms[i] + ","
            else:
                template_name += terms[i] + ","
        else:
            if not terms[i][0].isupper():
                template_name += "$" + terms[i] + ")"
            else:
                template_name += terms[i] + ")"
    return template_name


def groundedLiteralNameGenerator(f_name, terms):
    # This function receives the function name
    # and its terms and builds the whole name
    # for the grounded literal in the format
    #       'function(arg1,arg2)'
    name = f_name + "("

    for i in range(0, len(terms)):
        if i != len(terms) - 1:
            name += terms[i] + ","
        else:
            name += terms[i] + ")"
    return name


def generatePossibleSets(nterms, terms):
    # Generates all possible combinations of nterms with the
    # values supplied in terms recursively;
    # Returns the set as a list of lists
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
    # Receives a list with the intended set of constants
    # named comb, receives the arguments of the template
    # in args and the template in temp and then
    # performs the substitution, returning the obtained
    # string
    mapping = {}
    for i, arg in enumerate(args):
        mapping[arg] = comb[i]
    ident = string.Template(temp)
    name = ident.safe_substitute(mapping)
    return name

def generateBinaryTable(list):
    # Receives a list with all the possible names
    # for the actions after constant substitution and
    # computes the necessary number of binary variables
    # necessary to represent those actions and then
    # assigns one binary number to each action, returning
    # a dictionary named mapping whose keys are the actions'
    # names and the values are the assigned binary number
    nvars = len(list)
    nbin = math.ceil(math.log(nvars,2))
    if nbin == 0:
        nbin =1
    combinations = generatePossibleSets(nbin,[True,False])
    mapping={}
    for i,action_name in enumerate(list):
        if action_name not in mapping.keys():
            mapping[action_name] = combinations[i]
    return mapping



class Encoder(object):
    """docstring for Encoder"""

    def __init__(self, argv, bit):
        # This method initializes utility data and reads the input file;
        # It assumes all the constants of the problem are present in the
        # initial and goal states

        self.init = []  # initial state grounded literals
        self.goals = []  # goal state grounded literals
        self.sentence = []  # sentence at time t=h
        self.terms_list = []  # constants
        self.actions = []  # list of actions
        self.bitwise = bit # True = bitwise, False = classical
        self.mapping = {} # DIMACS mapping
        self.file_string = argv[1] # input file name
        self.discarded_actions = []
        self.predicates = []

        f = open(self.file_string, 'r') # open input file
        for line in f: # go through every line
            words = line.strip("\n").split()

            if line[0] == 'I': # if the line describes an initial state
                for arg in words[1:]:
                    name, terms = getFunctionNameTerms(arg)
                    for t in terms: # add new found constants to the list
                        if not (t in self.terms_list):
                            self.terms_list.append(t)
                    if not any( pred[0]==name for pred in self.predicates):
                        self.predicates.append([name,len(terms)])

                    if name[0] == "-":
                        signal = False
                        name = name[1:]
                    else:
                        signal = True
                    # generate the grounded literals for the initial state
                    ident = groundedLiteralNameGenerator(name, terms)
                    g_lit = GroundedLiteral(ident, signal)
                    self.init.append(g_lit)

            if line[0] == 'A': # if the line describes an action
                # separate the action part from the preconditions from the effects
                action_part = line[1:].strip(" ").split(":")[0]
                i_colon = line.index(":")
                i_arrow = line.index(">")
                precond_part = line[i_colon + 1:i_arrow - 1].strip("\n").split(" ")
                effect_part = line[i_arrow + 1:].strip("\n").split(" ")

                # Create an Action object from the action name and its template arguments
                action_name, action_terms = getFunctionNameTerms(action_part)
                template_name = templateNameCreator(action_name, action_terms)
                new_action = Action(template_name, action_terms)

                # Go through the preconditions
                for arg in precond_part:
                    if arg != "":
                        # Create an Atom object from the precondition's name and its template terms
                        precond_name, precond_terms = getFunctionNameTerms(arg)
                        if not any(pred[0] == precond_name for pred in self.predicates):
                            self.predicates.append([precond_name, len(precond_terms)])
                        template_name = templateNameCreator(precond_name, precond_terms)
                        new_atom = Atom(template_name, len(precond_terms))
                        new_action.addPreCondition(new_atom) # add precondition to the action
                        #print(template_name)
                # Go through the effects
                for arg in effect_part:
                    if arg != "":
                        # Create an Atom object from the effect's name and its template terms
                        effect_name, effect_terms = getFunctionNameTerms(arg)
                        name = effect_name
                        if name[0]=='-':
                           name = name[1:]
                        if not any(pred[0] == name for pred in self.predicates):
                            self.predicates.append([name, len(effect_terms)])
                        template_name = templateNameCreator(effect_name, effect_terms)
                        new_atom = Atom(template_name, len(effect_terms))
                        new_action.addEffect(new_atom) # add effect to the action
                        #print(template_name)
                self.actions.append(new_action)

            if line[0] == 'G': # if the line describes a ground state
                for arg in words[1:]:
                    name, terms = getFunctionNameTerms(arg)
                    # USE name and terms list here
                    for t in terms: # add new found constants to the list
                        if not (t in self.terms_list):
                            self.terms_list.append(t)
                    if not any(pred[0] == name for pred in self.predicates):
                        self.predicates.append([name, len(terms)])

                    if name[0] == "-":
                        signal = False
                        name = name[1:]
                    else:
                        signal = True
                    # Create the grounded literal for the goal state
                    ident = groundedLiteralNameGenerator(name, terms)
                    g_lit = GroundedLiteral(ident, signal)
                    self.goals.append(g_lit)
        f.close()

    def createIndexedActionLiteral(self, comb, action, sign, t):
        # Receives the action object, the list with the arguments to substitute
        # (comb), the sign intended for the grounded literal and the current
        # time step;
        # Performs substitution to get the literal name and then creates
        # the grounded literal and indexes the time step to its name;
        # Returns both the grounded literal and the obtained name
        name = mapAndSubstitute(comb, action.args, action.name_template)
        action_glit = GroundedLiteral(name, sign)
        action_glit.indexGL(t)
        return action_glit, name

    def initialStateClauses(self):
        # From the constructor of the Encoder class, the initial state
        # grounded literals are already available. This function computes
        # all the possible combinations of arguments for all those literals
        # and negates the ones that do not correspond to the initial state.
        # Additional loop control variables are inserted to guarantee that
        # grounded literals are not repeated since different grounded atoms in the
        # initial state can generate the same negated literal. In the end, both
        # the initial state literals and the negated ones are indexed with t=0
        # and added to the SAT sentence.
        to_append=[]
        for pred in self.predicates:
            combinations = generatePossibleSets(pred[1], self.terms_list)
            for comb in combinations:
                ident = groundedLiteralNameGenerator(pred[0], comb)
                if not any(ident==iglit.ident for iglit in self.init):
                    if not any(ident == aglit.ident for aglit in to_append):
                        g_lit = GroundedLiteral(ident, False)
                        to_append.append(g_lit)
        self.init.extend(to_append)
        # ninit = len(self.init)
        # for i in range(ninit):
        #     literal = self.init[i]
        #     name, args = getFunctionNameTerms(literal.ident)
        #     nargs = len(args)
        #     combinations = generatePossibleSets(nargs, self.terms_list)
        #     for comb in combinations:
        #         flag = False
        #         if comb != args:
        #             ident = groundedLiteralNameGenerator(name, comb)
        #             for glit in self.init:
        #                 if ident == glit.ident:
        #                     flag = True
        #                     break
        #             if flag:
        #                 continue
        #             else:
        #                 g_lit = GroundedLiteral(ident, not literal.signal)
        #                 self.init.append(g_lit)
        for literal in self.init:
            literal.indexGL(0)
            self.sentence.append([literal])

    def nameActions(self):
        # This function generates a list with the name of all possible
        # grounded actions
        actions_names = []
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                name = mapAndSubstitute(comb, action.args, action.name_template)
                actions_names.append(name)
        return actions_names

    def groundActionBits(self,bin_comb,t):
        # This function receives the binary number corresponding to a certain
        # grounded action (bitwise representation) and grounds every literal
        # (bit) in it to form the negated grounded action literal
        bits_list = []
        for i,bit in enumerate(bin_comb):
            name = 'b%s' % i
            bit_glit = GroundedLiteral(name, not bit)
            bit_glit.indexGL(t)
            bits_list.append(bit_glit)
        return bits_list

    def actionsImplications(self, t):
        # This function generates the clauses that correspond to the actions
        # implicating their preconditions and their effects;
        # It has condition statements in order to create the clauses
        # for the classical and the bitwise representation of actions;
        # Either way, what the function does is go through all the grounded actions
        # and create a clause with the negated action and a precondition or effect,
        # for every precondition and effect corresponding to that action;
        # Special care must be taken because in the actions' templates, the atoms
        # in the preconditions and effects can still have a negation operator in their
        # name strings;
        # Extra condition statements are added together with a loop control variable
        # named 'conflict' in order to avoid creating clauses corresponding to actions
        # that imply contradictory effects or contradictory preconditions; the way
        # this works is by keeping in memory, for a given grounded action, the effects
        # and the preconditions as the loop iterates through them to create the
        # clauses; if, during the loop, a conflict is found between the current
        # effect/precondition and another one already tested, then the clause that
        # is added to the sentence is merely '-A', where A is the corresponding
        # grounded action, because we know this action cannot be performed.
        if self.bitwise:
            mapping = generateBinaryTable(self.nameActions())
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                conflict = False
                efx_list=[]
                aglit, aname = self.createIndexedActionLiteral(comb, action, False, t)
                if self.bitwise:
                    bits_list = self.groundActionBits(mapping[aname], t)
                for effect in action.efx:
                    name = mapAndSubstitute(comb, action.args, effect.ident_template)
                    sign, name = effect.checkSign(name)
                    effect_glit = GroundedLiteral(name, sign)
                    effect_glit.indexGL(t + 1)
                    for added_glit in efx_list:
                        if effect_glit == -added_glit:
                            conflict = True
                            break
                    if conflict:
                        del(self.sentence[-len(efx_list):])
                        if self.bitwise:
                            self.sentence.append(bits_list)
                            self.discarded_actions.append(bits_list)
                        else:
                            self.discarded_actions.append(aglit)
                        break
                    else:
                        efx_list.append(effect_glit)
                        if self.bitwise:
                            self.sentence.append(bits_list + [effect_glit])
                        else:
                            self.sentence.append([aglit, effect_glit])
                if conflict:
                    continue
                precond_list = []
                for precond in action.preconds:
                    name = mapAndSubstitute(comb, action.args, precond.ident_template)
                    sign, name = precond.checkSign(name)
                    precond_glit = GroundedLiteral(name, sign)
                    precond_glit.indexGL(t)
                    for added_glit in precond_list:
                        if precond_glit == -added_glit:
                            conflict = True
                            break
                    if conflict:
                        del (self.sentence[-len(precond_list):])
                        if self.bitwise:
                            self.sentence.append(bits_list)
                            self.discarded_actions.append(bits_list)
                        else:
                            self.discarded_actions.append(aglit)
                        break
                    else:
                        precond_list.append(precond_glit)
                        if self.bitwise:
                            self.sentence.append(bits_list + [precond_glit])
                        else:
                            self.sentence.append([aglit, precond_glit])

    def propagateSteadyStates(self, t):
        # This function is responsible for creating the clauses corresponding to
        # the frame axioms, stating that literals unaffected by an action are kept
        # for the next time step;
        # A literal is considered to be unaffected by an action if it is different
        # from the grounded effects of that action;
        # This function has condition statements in order to work for both
        # classical and bitwise representation of actions;
        # The basic flow is to go through all the grounded actions and store in memory
        # all the grounded effects (in a dict called 'modified'). Then, for every
        # possible combination of arguments (for every atom in 'modified') that does
        # not correspond to an effect, a grounded literal is created. With this grounded
        # literal,'glit1', the clause '-A or -glit1 or glit2' is added to the sentence
        # with 'glit1' corresponding to time step t and 'glit2' to time step t+1;
        # Two clauses are created, with 'glit1' assuming a positive and a negative
        # sign and 'glit2' the opposite sign to 'glit1'.
        if self.bitwise:
            mapping = generateBinaryTable(self.nameActions())
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                aglit, aname = self.createIndexedActionLiteral(comb, action, False, t)
                if not self.bitwise:
                    if aglit in self.discarded_actions:
                        continue
                else:
                    bits_list = self.groundActionBits(mapping[aname], t)
                    if bits_list in self.discarded_actions:
                        continue
                modified = {}
                for effect in action.efx:
                    name = mapAndSubstitute(comb, action.args, effect.ident_template)
                    name = effect.checkSign(name)[1]
                    atom_name, terms = getFunctionNameTerms(name)
                    if atom_name in modified.keys():
                        modified[atom_name].append(terms)
                    else:
                        modified[atom_name] = [terms]
                for pred in self.predicates:
                    subset = generatePossibleSets(pred[1],self.terms_list)
                    for comb2 in subset:
                        if not (pred[0] in modified.keys() and comb2 in modified[pred[0]]):
                            name = groundedLiteralNameGenerator(pred[0], comb2)
                            for value in [True, False]:
                                glit1 = GroundedLiteral(name, value)
                                glit2 = -glit1
                                glit1.indexGL(t)
                                glit2.indexGL(t + 1)
                                if self.bitwise:
                                    self.sentence.append(bits_list + [glit1,glit2])
                                else:
                                    self.sentence.append([aglit, glit1, glit2])

    def areActionsConflicting(self,aglit1,aglit2):
        name1, terms1 = getFunctionNameTerms(aglit1.ident)
        name2, terms2 = getFunctionNameTerms(aglit2.ident)
        temp_dict = {aglit1.ident:[name1,terms1],aglit2.ident:[name2,terms2]}
        temp_efx={}
        temp_precond={}
        for action in self.actions:
            action_name = getFunctionNameTerms(action.name_template)[0]
            for key,val in temp_dict.items():
                name = val[0]
                if name == action_name:
                    for effect in action.efx:
                        ename =  mapAndSubstitute(val[1],action.args,effect.ident_template)
                        if key not in temp_efx.keys():
                            temp_efx[key]=[ename]
                        else:
                            temp_efx[key].append(ename)
                    for precond in action.preconds:
                        ename =  mapAndSubstitute(val[1],action.args,precond.ident_template)
                        if key not in temp_precond.keys():
                            temp_precond[key]=[ename]
                        else:
                            temp_precond[key].append(ename)
        res = False
        for ef1 in temp_efx[aglit1.ident]:
            ef1_is_neg = False
            if ef1[0]=='-':
                ef1_is_neg = True
                ef1 = ef1[1:]
            for ef2 in temp_efx[aglit2.ident]:
                ef2_is_neg = False
                if ef2[0] == '-':
                    ef2_is_neg = True
                    ef2 = ef2[1:]
                if ef1==ef2:
                    if (ef1_is_neg and not ef2_is_neg) or (not ef1_is_neg and ef2_is_neg):
                        res = True
                        return res
        for p1 in temp_precond[aglit1.ident]:
            p1_is_neg = False
            if p1[0] == '-':
                p1_is_neg = True
                p1 = p1[1:]
            for p2 in temp_precond[aglit2.ident]:
                p2_is_neg = False
                if p2[0] == '-':
                    p2_is_neg = True
                    p2 = p2[1:]
                if p1 == p2:
                    if (p1_is_neg and not p2_is_neg) or (not p1_is_neg and p2_is_neg):
                        res = True
                        return res
        return res


    def oneActionPerTimeStep(self, t):
        # This function is called when the classical representation for actions is
        # used. It consists of creating the at-least-one and at-most-one clauses
        # encompassing all grounded actions;
        # To create the at-least-one clause, it is only necessary to get all possible
        # grounded actions and create a clause as the disjunction of all those grounded
        # actions;
        # The at-most-one clause is a conjunction of clauses of two grounded actions
        # stating that for every pair of actions only one can occur (for the same time
        # step);
        # These clauses are created by creating a list with all grounded actions being negated
        # and then for every pair of them, create a clause like '-A1 or -A2' to stop both of them
        # from being True.
        at_least_one = []
        name_actions = self.nameActions()
        for action_name in name_actions:
            action_glit = GroundedLiteral(action_name, True)
            action_glit.indexGL(t)
            if -action_glit not in self.discarded_actions:
                at_least_one.append(action_glit)
        self.sentence.append(at_least_one)

        # At most one action per time step
        alist = []
        for action in self.actions:
            nargs = len(action.args)
            combinations = generatePossibleSets(nargs, self.terms_list)
            for comb in combinations:
                a = self.createIndexedActionLiteral(comb, action, False, t)[0]
                if a in self.discarded_actions:
                    continue
                alist.append(a)
        for i, a1 in enumerate(alist):
            for j, a2 in enumerate(alist):
                if j > i and not self.areActionsConflicting(a1,a2):
                    self.sentence.append([a2, a1])

    def negateUnassignedActions(self,t):
        # This function is used only for the bitwise representation
        # of actions;
        # It is necessary because the chosen number of bits to represent
        # all grounded actions may result in a number of combinations
        # greater than the number of grounded actions, leaving some
        # binary numbers with no corresponding action. This can be
        # problematic if the SAT solver solution returns an assignment
        # for these bits that doesn't correspond to any action, meaning
        # the goal state may not have any conflict at time step 1;
        # For this reason, the unassigned binary sequences must correspond
        # to clauses that make those sequences False
        list_actions = self.nameActions()
        mapping = generateBinaryTable(list_actions)
        nvars = len(list_actions)
        nbin = math.ceil(math.log(nvars, 2))
        if nbin == 0:
            nbin = 1
        combinations = generatePossibleSets(nbin, [True, False])
        for comb in combinations:
            if comb not in mapping.values():
                bits_list = self.groundActionBits(comb, t)
                self.sentence.append(bits_list)

    def addGoalStates(self, t):
        # This function simply adds the goal state's literals
        # to the SAT sentence, indexed by (t+1) at time t, i.e.,
        # at least one action is necessary to reach the goal state
        for literal in self.goals:
            glit = copy.copy(literal)  # copy instead of deepcopy because GroundedLiteral doesnt have objects in it
            glit.indexGL(t + 1)
            self.sentence.append([glit])

    def removePreviousGoalStates(self):
        # If the SAT sentence generator is being called at time
        # t, then it means the problem wasn't satisfiable at time
        # (t-1), so we need to remove the goal state's literals
        # from the previous time step.
        # This is easily done by assuming the goal state's clauses
        # are always on the end of the SAT sentence.
        nlits = len(self.goals)
        del (self.sentence[-nlits:])

    def translateDIMACS(self,t):
        # This function takes the generated SAT sentence
        # and assigns an integer to every atom in it;
        # It then goes through the sentence again to
        # write every clause in it in a file using the
        # integer assignment created before, negating the
        # values for negated literals.
        lits = [l for c in self.sentence for l in c]
        self.mapping = {}
        for lit in lits:
            if lit.ident not in self.mapping.keys():
                self.mapping[lit.ident] = len(self.mapping) + 1
        filename = 'dimacs' + '.dat'#('_%s'%t) + '.dat'
        f = open(filename, 'w')
        f.write('c 75398 76312\n')
        nvars = len(self.mapping)
        nclauses = len(self.sentence)
        f.write('p cnf %s %s\n' % (nvars, nclauses))
        for clause in self.sentence:
            string = ''
            for lit in clause:
                if lit.signal == False:
                    string += '-'
                string += ('%s ' % self.mapping[lit.ident])
            string += '0' + '\n'
            f.write(string)
        f.close()

    def generateSentence(self, t):
        # This is the function that generates the SAT sentence to
        # be fed to the SAT solver.
        if t == 0:
            # First, create unit clauses for the initial state
            self.initialStateClauses()
        else:
            # Remove goal state clauses from previous time step
            self.removePreviousGoalStates()
        # Actions imply their preconditions and effects
        self.actionsImplications(t)
        # Atoms not modified by an action are propagated in time
        self.propagateSteadyStates(t)
        if self.bitwise:
            # If using bitwise representation, negate the unused assignments
            self.negateUnassignedActions(t)
        else:
            # One action per time step clauses for classical representation of actions
            self.oneActionPerTimeStep(t)
        # Goal is reached in time horizon h = t+1
        self.addGoalStates(t)
        # Translate to the DIMACS format
        self.translateDIMACS(t)

    def printSolution(self,t,Sol):
        # This function is responsible for reading the list
        # with the solution from the SAT solver and for
        # interpreting the result in order to retrieve the actions
        # that have been assigned True in the solution;
        # It has two different approaches for bitwise and classical
        # representation of actions, but the idea is to get all the variables
        # that have been assigned True and look for the ones that correspond
        # to actions and then fetch the correct name of the action and print
        # in the display from t=0 to t=h

        if Sol[0] == 'UNSAT': # if unsatisfiable, exit
            return False
        vars = []
        for arg in Sol[1:]:
            if int(arg) > 0:
                vars.append(int(arg)) # take variables assigned with True
        print('-----------------')
        print('Problem solution:')
        print('-----------------')
        if self.bitwise: # for the bitwise representation of actions
            list_actions = self.nameActions() # get actions' names
            bin_table = generateBinaryTable(list_actions) # generate mapping actions-binary numbers
            nbits = len(list(bin_table.values())[0])
            for h in range(t + 1):
                current_action = [False] * nbits
                for var in vars: # for every variable assigned True
                    for name, num in self.mapping.items(): # for every correspondence in DIMACS mapping
                        if num == var and name[0] == 'b' and int(name[-1]) == h:
                            # if it is an action bit at time t=h
                            bit_index = int(name[1]) # get bit index
                            current_action[bit_index] = True # build the action binary sequence
                for action_name, bits in bin_table.items(): # search for the sequence obtained
                    if bits == current_action: # if we found the sequence...
                        name = action_name # ... we found the corresponding action
                        break
                print(name)
        else: # for the classical representation of actions
            action_names = []
            for action in self.actions: # get the name of the actions (without arguments)
                action_names.append(getFunctionNameTerms(action.name_template)[0])
            for h in range(t+1): # search for every time step
                for var in vars: # check every variable assigned True by the solver
                    for name, num in self.mapping.items(): # check the DIMACS mapping
                        if num == var: # if a certain number is True...
                            pred_or_action_name = getFunctionNameTerms(name)[0]#...get name for that number
                            if pred_or_action_name in action_names and int(name[-1]) == h:
                                # ...and if it is an action (not a predicate) at time=h , then print
                                print(name[:-2])
        return True


