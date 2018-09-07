from generators.generator import generator
from core.single import satransform
from core.transform import noop
from quality.logic import *
import itertools

class dedup(generator):

    def __init__(self, relation, generatorParams):
        super(dedup, self).__init__(relation, generatorParams)

    def _getAttributeInt(self, attr):
        yield from []

    def _getAttribute(self, attr):
        for sim, thresh in self.generatorParams:

            xform = noop()

            for tup in self._attrPairIterator(attr):
                if sim(tup[0],tup[0]) < thresh:
                    xform = satransform(attr, tup[0], tup[1], EQ) + xform

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




