from generators.generator import generator
from core.single import satransform
from core.transform import noop
from quality.logic import *
import itertools
import random
import sys

class minhash(generator):

    def __init__(self, relation, generatorParams):
        super(minhash, self).__init__(relation, generatorParams)

    def _getAttributeInt(self, attr):
        yield from []

    def hash(self,string, modulo):
        return id(string) % modulo

    def genFamily(self, k):
        rtn = []
        for i in range(0,k):
            rtn.append(lambda s: self.hash(s, random.randint(k, k**2) ))
        return rtn

    def shingle(self, st, k):
        shingles = []
        for i in range(k, len(st)+1,1):
            shingles.append(st[i-k:i])

        return shingles

    def minHash(self, shingles, hashFamily):
        argmin = sys.maxsize

        for shingle in shingles:
            for h in hashFamily:
                argmin = min(argmin, h(shingle))

        return argmin

    def _getAttribute(self, attr):

        for sszie, hsize in self.generatorParams:
            
            dup = {}
            hf = self.genFamily(1)
            xform = noop()

            for s in self._attrVals(attr):
                v = self.minHash(self.shingle(s,2), hf)

                if v not in dup:
                     dup[v] = []
                
                dup[v].append(s)

            for v in dup:
                if len( dup[v]) > 1:
                    for s in  dup[v]:
                        xform = satransform(attr, s,  dup[v][0], EQ) + xform

            yield xform

    def get(self):
        iterlist = []
        for attr,t in zip(self.data.attrs, self.data.types):
            if t == 'num':
                for t in self._getAttributeInt(attr):
                    yield t
            else:
                for t in self._getAttribute(attr):
                    yield t




