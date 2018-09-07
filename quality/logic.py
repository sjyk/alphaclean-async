"""
Module defines basic logical building blocks for writing rules
"""


#boolean logic
def implies(a,b):
    return (not a) or b

def xor(a,b):
    return (a and not b) or (not a and b)

def iff(a,b):
    return implies(a,b) and implies(b,a)





#tuple logic
EQ, GT, GTE, LT, LTE, NE = (0,1,2,3,4,5)


