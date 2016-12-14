from SatSolver import *
import time
import random

def decideBranch(clauses,branched, symbols, model):
    if symbols is not None and len(symbols) > 0:
        max_heuristic=[None,-10,None] #Symbol;Heuristic

        for result in symbols:
            # h=heuristicJW(clauses,s,model)
            # if h>max_heuristic[1]:
            #     max_heuristic[0]=s
            #     max_heuristic[1]=h
            #     max_heuristic[2]=True

            # h=heuristicJW(clauses,s,model,False)
            # if h>max_heuristic[1]:
            #     max_heuristic[0]=s
            #     max_heuristic[1]=h
            #     max_heuristic[2]=False

            # signal=max_heuristic[2]
            # result=max_heuristic[0]
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


def deduceStatus(changed,clauses, symbols, model):
    changes = []

    if isEveryClauseTrue(clauses, model):
        model.success = True
        return ["SAT", changes]

    res, clause = isAnyClauseFalse(clauses, model)
    
    if res:
        #learnConflict(clause,clauses,changed,model)
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

def learnConflict(con_clause,clauses,changed,model): 
    new_clause=[]
    for l in con_clause:
        for key in changed.keys():
            if l.name in changed[key]:
                new_clause.append(Variable(changed[key][0],not model[changed[key][0]]))
                break
    # for key in changed.keys():
    #     if key > 0:
    #        new_clause.append(Variable(changed[key][0],not model[changed[key][0]])) 
    clauses.append(new_clause)


def heuristicDLIS(clauses,symb,model,signal=True):
    h=0
    for c in clauses:
        if isClauseActive(c,model):
            if any(l.name==symb and l.signal==signal for l in c):
                h+=1
    return h
def heuristicJW(clauses,symb,model,signal=True):
    h=0
    for c in clauses:
        if isClauseActive(c,model):
            if any(l.name==symb and l.signal==signal for l in c):
                h+=2**(-len(c))
    return h

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

