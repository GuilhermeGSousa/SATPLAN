from SatSolver import *
import time
import random

#Decides next assignment based on previous branches
def decideBranch(clauses,branched, symbols, model):
    if symbols is not None and len(symbols) > 0:
        max_heuristic=[None,-10,None] #Symbol;Heuristic

        for result in symbols:

            signal=False

            if branched.keys() is None or result not in branched.keys():
                symbols.remove(result)
                model[result] = signal
                branched[result] = [signal]
                return [result, signal]

            elif len(branched[result])==1:
                symbols.remove(result)
                model[result] = not branched[result][0]
                branched[result].append(not branched[result][0])
                return [result, not branched[result][0]]

    return [None, False]

#Propagates constraints and checks for conflicts and solved problem
def deduceStatus(changed,clauses, symbols, model):
    changes = []

    if isEveryClauseTrue(clauses, model):
        model.success = True
        return ["SAT", changes]

    res, clause = isAnyClauseFalse(clauses, model)
    
    if res:
        learnConflict(clause,clauses,changed,model)
        model.success = False
        return ["CONFLICT", changes]

    if symbols is not None:
        for s in symbols:
            res, val = isPureSymbol(clauses, s, model)
            if res:
                symbols.remove(s)
                model[s] = val
                changes.append(s)
                continue
    change = assignUnitSymbols(clauses, symbols, model)

    if change is not None:
        changes.extend(change)
        return ["OTHER", changes]
    else:
        return ["BRANCH",changes]

#Learns from a conflict and adds a clause to clauses list
def learnConflict(con_clause,clauses,changed,model): 
    new_clause=[]
    for l in con_clause:
        for key in changed.keys():
            if l.name in changed[key]:
                new_clause.append(Variable(changed[key][0],not model[changed[key][0]]))
                break 
    clauses.append(new_clause)


#Returns value from heuristic
def heuristicJW(clauses,symb,model,signal=True):
    h=0
    for c in clauses:
        if isClauseActive(c,model):
            if any(l.name==symb and l.signal==signal for l in c):
                h+=2**(-len(c))
    return h

#Returns backtrack level based on conflict
def analyzeConflict(branched, changed, model, lvl):

    if changed[lvl][0]!=[] and len(branched[changed[lvl][0]])==1:
        return lvl - 1
    else:
        steps_back = 1
        while True:
            blvl = lvl - steps_back - 1
            if blvl < 0:
                return blvl
            previous_symb = changed[lvl - steps_back][0]
            if len(branched[previous_symb]) == 1:
                return blvl
            steps_back += 1

#Backtracks model to a given decision level
def backtrackToLevel(branched, changed, symbols, model, blvl, lvl):
    for i in range(lvl, blvl, -1):
        symbol = changed[i][0]
        if i > 0:
            for j, s in enumerate(changed[i]):
                if j == 0:
                    symbols.insert(0, s)
                else:
                    symbols.append(s)
                del model.var_sol[s]
            del changed[i]
        if i > blvl + 1:
            del branched[symbol]

#Iterative DPLL algorithm
def solveIterativeCNF(clauses, symbols, model=Solution()):
    branched = {}
    changed = {}
    lvl = 0
    backtracks = 0
    count = 0

    changed[0] = deduceStatus(changed, clauses, symbols, model)[1]

    while True:

        symb, val = decideBranch(clauses,branched, symbols, model)  # Implement heuristic here

        if symb is not None:
            lvl = lvl + 1
            changed[lvl] = [symb]

            
        status, changes = deduceStatus(changed,clauses, symbols,
                                       model)  
        if lvl > 0:
            changed[lvl].extend(changes)
        print(status)

        if status == "CONFLICT":
            count += 1
            blvl = analyzeConflict(branched, changed, model, lvl)
            if blvl < 0:
                return [False, model]
            
            # if backtracks>1:
            #     print("Restarting")
            #     backtrackToLevel(branched,changed,symbols,model,0,lvl)
            #     backtracks=0
            #     tmp=changed[0]
            #     changed.clear()
            #     changed[0]=tmp
            #     lvl=0
            # else:
            #     backtracks+=1
            backtrackToLevel(branched, changed, symbols, model, blvl, lvl)
            lvl = blvl
        elif status == "SAT":
            return [True, model]
        else:
            pass

