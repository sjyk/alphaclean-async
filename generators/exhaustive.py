from generators.generator import generator
from core.single import satransform
from quality.logic import *
import itertools

class exhaustive(generator):

    def __init__(self, relation, generatorParams):
        super(exhaustive, self).__init__(relation, generatorParams)


    def _getAttributeInt(self, attr):
        for v in self._attrVals(attr):
            yield satransform(attr, v, None, EQ)
            yield satransform(attr, v, None, GT)
            yield satransform(attr, v, None, LT)

    def _getAttribute(self, attr):
        for tup in self._attrPairIterator(attr):
            yield satransform(attr, tup[0], tup[1], EQ)

    def get(self):
        iterlist = []
        for attr,t in zip(self.data.attrs, self.data.types):
            if t == 'num':
                for t in self._getAttributeInt(attr):
                    yield t
            else:
                for t in self._getAttribute(attr):
                    yield t




