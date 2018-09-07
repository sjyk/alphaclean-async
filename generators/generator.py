from core.single import satransform
from core.transform import noop

class generator(object):

    def __init__(self, relation, generatorParams):
        self.data = relation
        self.generatorParams = generatorParams


    def _attrPairIterator(self, attr):
        for i in self.data.scanDistinct(attr):
            for j in self.data.scanDistinct(attr):
                yield i,j

    def _attrVals(self, attr):
        for i in self.data.scanDistinct(attr):
            yield i

    def get(self):
        raise NotImplemented("get() implemented in subclasses")

    def score(self, qfn, base):
        for xform in self.get():
            compound = xform + base
            relCpy = compound.apply(self.data)
            yield (qfn.run(relCpy), compound)


    def bbrun(self):
        xform = noop()
        for newXform in self.get():
            xform = newXform + xform

        return xform


    def __add__(self, other):

        for i in self.get():
            yield i

        for j in other.get():
            yield j




