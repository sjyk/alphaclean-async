import copy
from core.transform import transform
from quality.logic import *

"""
Represents single attribute transforms
"""
class satransform(transform):

    def __init__(self, attr, src, target, op):

        opFn = self.translate(op)
        srcFn = lambda s: opFn(s[attr],src)

        self.attr = attr
        self.src = src
        self.target = target

        super(satransform, self).__init__(srcFn, attr, target)


    def translate(self,op):

        if op == EQ:
            return lambda s,t: (s != None) and (t != None) and s == t
        elif op == GT:
            return lambda s,t: (s != None) and (t != None) and s > t
        elif op == GTE:
            return lambda s,t: (s != None) and (t != None) and s >= t
        elif op == LT:
            return lambda s,t: (s != None) and (t != None) and s < t
        elif op == LTE:
            return lambda s,t: (s != None) and (t != None) and s <= t
        elif op == NE:
            return lambda s,t: (s != None) and (t != None) and s != t
        else:
            return lambda s,t: False

    def __str__(self):
        return str(self.attr) + ":" + str(self.src) +"=>"+ str(self.target) 