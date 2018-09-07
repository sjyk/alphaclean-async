import copy
"""
A relation to relation mapping per tuple
"""
class transform(object):

    def __init__(self, conditionList, targetAttrList, targetValueList):

        if not isinstance(conditionList,(list,)):
            conditionList = [conditionList]

        if not isinstance(targetValueList,(list,)):
            targetValueList = [targetValueList]

        if not isinstance(targetAttrList,(list,)):
            targetAttrList = [targetAttrList]

        self.condition = conditionList
        self.targetAttr = targetAttrList
        self.targetValue = targetValueList


    def apply(self, relation):
        
        relationCpy = copy.deepcopy(relation)

        for row in relationCpy.scan():
            for cond, attr, val in zip(self.condition, self.targetAttr, self.targetValue):
                if cond(row):
                    row[attr] = val

        return relationCpy

    def __add__(self, other):
        return transform(self.condition+other.condition, 
                        self.targetAttr + other.targetAttr, 
                        self.targetValue+other.targetValue)


class noop(transform):

    def __init__(self):
        super(noop, self).__init__(lambda s: False, '', None)

    def apply(self, relation):
        return copy.deepcopy(relation)

"""
class transformSet(object):

    def __init__(self, xforms):
        self.xforms = xforms

    def score(self, rel, qfn):
        for xform in self.xforms:
            relCpy = xform.apply(rel)
            yield (qfn.run(relCpy), xform)

    def __add__(self, other):
        return transformSet(other.xforms + self.xforms)
"""
