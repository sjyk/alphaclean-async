from quality.qfn import qfn
from quality.logic import *

"""
A denial constraint is a special class of quality function
"""
class dc(qfn):

    """
    A denial constraint takes in a specific form of quality fn
    over tuples of rows
    """
    def __init__(self, function):

        def self_join(relation):
            count = 0

            for s,t in relation.n_way_cartesian(2):
                if (str(s) != str(t)):
                    count +=  (not function(s,t))

            return count

        super(dc, self).__init__(self_join)


"""
A functional depdency is a special kind of denial constraint
"""
class fd(dc):

    """
    A functional dependency takes in two lists of attributes
    """
    def __init__(self, a, b):

        def all_equal(s, t, attrList):

            for attr in attrList:
                if s[attr] != t[attr]:
                    return False

            return True

        super(fd, self).__init__(lambda s,t: implies(all_equal(s,t,a), all_equal(s,t,b) ))


"""
A matching depdency is a special kind of denial constraint
"""
class md(dc):

    """
    Takes in a similarity function, attributes, and threshold below which considers a match
    """
    def __init__(self, sim, attrs, thresh):

        def sp(r, attrList):
            rtn = ""
            for a in attrList:
                rtn += r[a] + " "
            return rtn

        def all_equal(s, t, attrList):

            for attr in attrList:
                if s[attr] != t[attr]:
                    return False

            return True

        super(md, self).__init__(lambda s,t: implies(sim(sp(s,attrs), sp(t,attrs)) <= thresh, all_equal(s,t,attrs) ))
