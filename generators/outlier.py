from generators.generator import generator
from core.single import satransform
from quality.logic import *
import itertools
import numpy as np

class outlier(generator):

    def __init__(self, relation, generatorParams):
        super(outlier, self).__init__(relation,generatorParams)


    def _getAttributeInt(self, attr):
        numberArray = np.array([v for v in self._attrVals(attr)])
        mean = np.mean(numberArray)
        std = np.std(numberArray)

        for thresh in self.generatorParams:
            yield satransform(attr, mean + thresh*std, None, GT)
            yield satransform(attr, mean - thresh*std, None, LT)

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




