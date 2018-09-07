"""
This defines the main class for a quality function, 
basically allows for linear combinations of abstract
quality functions.
"""
class qfn(object):

    """
    A quality function takes in a function as input
    """
    def __init__(self, function):
        self.run = function


    """
    Scalar multiply
    """
    def __rmul__(self, other):
        return qfn( lambda rel: other*self.run(rel) )


    """
    Add two quality functions together
    """
    def __add__(self, other):
        return qfn( lambda rel: other.run(rel) + self.run(rel) )



class pointwise(qfn):

    def __init__(self, rowFunction, skipNull=False):
        
        def scan(relation):
            count = 0
            for s in relation.scan():

                try:
                    count += rowFunction(s)
                except Exception:
                    count += skipNull

            return count

        super(pointwise, self).__init__(scan)
