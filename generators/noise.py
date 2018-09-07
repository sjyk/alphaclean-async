from generators.generator import generator
from core.single import satransform
from quality.logic import *
import itertools
import numpy as np
import random

class noise(generator):

    def __init__(self, relation, generatorParams):
        super(noise, self).__init__(relation,generatorParams)


    def _getAttributeInt(self, attr):
        for v in self._attrVals(attr):
            yield satransform(attr, v, random.random()*self.generatorParams[0], EQ)

    def _getAttribute(self, attr):
        yield from []

    def get(self):
        iterlist = []
        for attr,t in zip(self.data.attrs, self.data.types):
            if t == 'num':
                for t in self._getAttributeInt(attr):
                    yield t
            else:
                for t in self._getAttribute(attr):
                    yield t




