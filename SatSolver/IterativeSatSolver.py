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


def deduceStatus(clauses, symbols, model):
    changes = []

    if isEveryClauseTrue(clauses, model):
        model.success = True
        print("all true")
        return ["SAT", changes]

    res, clause = isAnyClauseFalse(clauses, model)
    if res:
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


def analyzeConflict(branched, changed, clauses, model, lvl):
    # learnConflict(clauses,model)
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


def backtrackToLevel(branched, changed, symbols, symb, model, blvl, lvl):
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
    while True:
        print(len(symbols))
        # for Var, Val in model.var_sol.items():
        #     if Val is None:
        #         print(Var)
        vec= [1,2,3,4,22,23,24,25,26,30,31,34,38,43,48,49,52,53,54,57,
              60,61,63,70,75,77,80,87,88,89,90,95]
        if all(y in model.var_sol.values() for y in vec):
            if all(model.var_sol[x]==True for x in vec):
                print('*********************************')
        if None in model.var_sol.values():
            print('---------------------------------')
        symb, val = decideBranch(branched, symbols, model)  # Implement heuristic here

        if symb is not None:
            lvl = lvl + 1
            changed[lvl] = [symb]
        while True:
            status, changes = deduceStatus(clauses, symbols,
                                           model)  # This function takes the longest to run for large input files
            if lvl > 0:
                changed[lvl].extend(changes)
            print(status)
            if status == "CONFLICT":
                count += 1
                blvl = analyzeConflict(branched, changed, clauses, model, lvl)
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
                backtrackToLevel(branched, changed, symbols, symb, model, blvl, lvl)
                lvl = blvl
                break
            elif status == "SAT":
                return [True, model]
            else:
                break
