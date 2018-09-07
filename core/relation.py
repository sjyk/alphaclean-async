import itertools

"""
A relation is a list of dictionaries
"""
class relation(object):

    def __init__(self, data, attrs=None):
        self.data = data
        
        if attrs == None:
            self.attrs = list(data[0].keys())
        else:
            self.attrs = list(attrs)


    def setTypes(self, typeList):
        if len(typeList) != len(self.attrs):
            raise ValueError("Incomplete Type Spec")

        self.types = list(typeList)

    """
    returns an iterator over rows
    """
    def scan(self):
        for element in self.data:
            yield element

    def scanDistinct(self, attr):
        scanned = set()
        for element in self.data:
            if not element[attr] in scanned:
                yield element[attr]

            scanned.add(element[attr])

    """
    returns an iterator over tuples of data
    """
    def n_way_cartesian(self, n):
        tuples = [self.data]*n
        for element in itertools.product(*tuples):
            yield element


    def __str__(self):
        return str(self.data)

