


values = [True, False]

for v in values:
    b1 = v
    for v2 in values:
        b2 = v2
        res1 = (b1 and b2) or (not b1 and b2) or (not b1 and not b2) or (b1 and not b2)
        res2 = (b2 or b1) and (not b1 or not b2)
        print(res1)
        print(res2)
        print('----')
