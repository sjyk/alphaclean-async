from core.transform import noop
import datetime
import itertools
import random
import sys

class search(object):

    def __init__(self, data, qfn, generatorDesc, generatorParams, maxDepth=1, thresh=0):
        self.data = data
        self.qfn = qfn

        if not isinstance(generatorDesc,(list,)):
            generatorDesc = list([generatorDesc])

        self.generator = generatorDesc
        self.thresh = thresh
        self.maxDepth = maxDepth
        self.search_stats = {}
        self.params = generatorParams

    def _runIter(self, data, init=noop()):
        xform = init
        value = self.qfn.run(xform.apply(data))

        for g,p in zip(self.generator,self.params):
            gen = g(data,p)

            if value == 0:
                break

            for score, newXform in gen.score(self.qfn, xform):

                if value == 0:
                    break

                if score < value:
                    xform = newXform
                    value = score

        return (value, xform)


    def run(self):
        init = noop()
        data = init.apply(self.data)

        startTime = datetime.datetime.now()

        for i in range(self.maxDepth):
            value, xform = self._runIter(data, init)
            data = xform.apply(data)
            init = xform + init

            if value == 0: 
                break

        self.search_stats['runtime'] = (datetime.datetime.now() - startTime).total_seconds()

        return (value, xform, data)

class greedysearch(object):

    def __init__(self, data, qfn, generatorDesc, generatorParams):
        self.data = data
        self.qfn = qfn

        if not isinstance(generatorDesc,(list,)):
            generatorDesc = list([generatorDesc])

        self.generator = generatorDesc
        self.search_stats = {}
        self.params = generatorParams

    def run(self):
        init = noop()
        data = init.apply(self.data)
        value = self.qfn.run(init.apply(data))
        

        startTime = datetime.datetime.now()

        for g,p in zip(self.generator,self.params):

            argvalue = sys.maxsize
            argmax = noop()

            for instance in p:
                gen = g(data, list([instance]) )
                xform = gen.bbrun()
                newValue = self.qfn.run(xform.apply(data))

                if newValue < argvalue:
                    value = newValue
                    argmax = xform

            init = argmax + init


        self.search_stats['runtime'] = (datetime.datetime.now() - startTime).total_seconds()

        return (value, init, data)

class rgreedysearch(object):

    def __init__(self, data, qfn, generatorDesc, generatorParams):
        self.data = data
        self.qfn = qfn

        if not isinstance(generatorDesc,(list,)):
            generatorDesc = list([generatorDesc])

        self.generator = generatorDesc
        self.search_stats = {}
        self.params = generatorParams

    def run(self):
        init = noop()
        data = init.apply(self.data)
        value = self.qfn.run(init.apply(data))
        argmax = noop()

        startTime = datetime.datetime.now()

        for g,p in zip(self.generator,self.params):

            for instance in p:
                gen = g(data, list([instance]) )
                xform = gen.bbrun() + init
                newValue = self.qfn.run(xform.apply(data))

                if newValue < value:
                    value = newValue
                    argmax = xform

            init = argmax


        self.search_stats['runtime'] = (datetime.datetime.now() - startTime).total_seconds()

        return (value, init, data)



class gridsearch(object):

    def __init__(self, data, qfn, generatorDesc, generatorParams):
        self.data = data
        self.qfn = qfn

        if not isinstance(generatorDesc,(list,)):
            generatorDesc = list([generatorDesc])

        self.generator = generatorDesc
        self.search_stats = {}
        self.params = generatorParams

    def run(self):
        init = noop()
        data = init.apply(self.data)
        value = self.qfn.run(init.apply(data))
        

        startTime = datetime.datetime.now()

        for element in itertools.product(*self.params):
            argmax = noop()

            for i in range(0, len(self.params)):
                g = self.generator[i](data, list([element[i]]))

                t = g.bbrun()
                prior = self.qfn.run(argmax.apply(data))
                argmax =  t + argmax
                post = self.qfn.run(argmax.apply(data))

                if post > prior:
                    argmax = t

            newValue = self.qfn.run(argmax.apply(data))
            
            if newValue < value:
                value = newValue
                init = argmax

        self.search_stats['runtime'] = (datetime.datetime.now() - startTime).total_seconds()

        return (value, init, data)


class randomsearch(object):

    def __init__(self, data, qfn, generatorDesc, generatorParams, count=3):
        self.data = data
        self.qfn = qfn

        if not isinstance(generatorDesc,(list,)):
            generatorDesc = list([generatorDesc])

        self.generator = generatorDesc
        self.count = count
        self.search_stats = {}
        self.params = generatorParams

    def run(self):
        init = noop()
        data = init.apply(self.data)
        value = self.qfn.run(init.apply(data))
        
        startTime = datetime.datetime.now()

        evalcount = 0

        paramSettings = [element for element in itertools.product(*self.params)]
        random.shuffle(paramSettings)

        for element in paramSettings:

            argmax = noop()
            for i in range(0, len(self.params)):
                g = self.generator[i](data, list([element[i]]))

                t = g.bbrun()
                prior = self.qfn.run(argmax.apply(data))
                argmax =  t + argmax
                post = self.qfn.run(argmax.apply(data))

                if post > prior:
                    argmax = t

            newValue = self.qfn.run(argmax.apply(data))
            
            if newValue < value:
                value = newValue
                init = argmax

            if evalcount >= self.count:
                break

            evalcount += 1

        self.search_stats['runtime'] = (datetime.datetime.now() - startTime).total_seconds()

        return (value, init, data)




