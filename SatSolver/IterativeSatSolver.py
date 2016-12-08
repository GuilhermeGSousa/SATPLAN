from SatSolver import *
import time


def decideBranch(branched, symbols, model):
    if symbols is not None and len(symbols) > 0:

        for s in symbols:

            if branched.keys() is None:
                val = s
                symbols.remove(s)
                model[val] = False
                branched[val] = False
                return [val, False]

            if s not in branched.keys():
                val = s
                symbols.remove(s)
                model[val] = False
                branched[val] = False
                return [val, False]

            if branched[s] == False:
                val = s
                symbols.remove(s)
                model[val] = True
                branched[val] = True
                return [val, True]

    return [None, False]


def deduceStatus(changed,clauses, symbols, model):
    changes = []

    if isEveryClauseTrue(clauses, model):
        model.success = True
        print("all true")
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
                # res, val = isUnitClause(clauses,s,model)
                # if res:
                # 	symbols.remove(s)
                # 	model[s]=val
                # 	changes.append(s)
                # 	continue
    change = assignUnitSymbols(clauses, symbols, model)

    if change is not None:
        changes.extend(change)

    return ["OTHER", changes]

def learnConflict(con_clause,clauses,changed,model): 
    new_clause=[]

    for l in con_clause:
        for key in changed.keys():
            if l.name in changed[key]:
                new_clause.append(Variable(changed[key][0],not model[changed[key][0]]))
                break

    clauses.append(new_clause)

def analyzeConflict(branched, changed, model, lvl):
    if branched[changed[lvl][0]] == False:
        return lvl - 1
    else:
        steps_back = 1
        while True:
            blvl = lvl - steps_back - 1
            if blvl < 0:
                return blvl
            previous_symb = changed[lvl - steps_back][0]
            if branched[previous_symb] == False:
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
        symb, val = decideBranch(branched, symbols, model)  # Implement heuristic here

        if symb is not None:
            lvl = lvl + 1
            changed[lvl] = [symb]
        while True:
            status, changes = deduceStatus(changed,clauses, symbols,
                                           model)  # Th'is function takes the longest to run for large input files
            if lvl > 0:
                changed[lvl].extend(changes)
            print(status)
            if status == "CONFLICT":
                count += 1
                blvl = analyzeConflict(branched, changed, model, lvl)
                if blvl < 0:
                    return [False, model]

                # if backtracks>=20:
                # 	print("Restarting")
                # 	backtrackToLevel(changed,symbols,model,0,lvl)
                # 	backtracks=0
                # 	# changed={}
                # 	lvl=0
                # else:
                # 	backtracks+=1
                backtrackToLevel(branched, changed, symbols, model, blvl, lvl)
                lvl = blvl
                break
            elif status == "SAT":
                return [True, model]
            else:
                break
